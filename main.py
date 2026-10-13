import os
import argparse
import sys
from dotenv import load_dotenv
from openai import OpenAI

from prompts import system_prompt

from functions.call_function import call_function
from call_functions import available_functions

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key is None:
    raise RuntimeError("no openrouter api key")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)


def main():

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    verbose = args.verbose

    messages = [
        {"role": "system", "content": system_prompt },
        {"role": "user", "content": args.user_prompt},
    ]

    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
            temperature=0
        )

        if response.usage is None: 
            raise RuntimeError("error getting a response")

        if verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")


        message = response.choices[0].message
        messages.append(message)

        if not message.tool_calls:
            print(message.content)
            break

        for tool_call in message.tool_calls:
            result = call_function(tool_call, verbose)
            if not result.get("content"):
                raise RuntimeError(f"Empty function response for {tool_call.function.name}")

            if verbose:
                print(f"-> {result['content']}")

            messages.append(result)
        
    else:
        print("Error: maximum number of iterations (20) reached without a final response.")
        sys.exit(1)


if __name__ == "__main__":
    main()

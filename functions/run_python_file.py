import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes or Runs a specified Python file within the working directory and returns its output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to run, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of arguments to pass to the Python script",
                },
            },
            "required": ["file_path"],
        },
    },
}

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
        try:
            abs_working_dir = os.path.abspath(working_directory)
            abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
            is_outside_of_working_directory = os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir

            if is_outside_of_working_directory:
                return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
                        
            if not os.path.isfile(abs_file_path):
                return f'Error: "{file_path}" does not exist or is not a regular file'

            if not abs_file_path.endswith(".py"):
                 return f'Error: "{file_path}" is not a Python file'

            commands = ["python", abs_file_path]

            if args is not None and len(args) > 0:
                 commands.extend(args)


            result = subprocess.run(commands, capture_output=True, text=True, timeout=30)
            
            output: list[str] = []
            if result.returncode != 0:
                output.append(f"Process exited with code {result.returncode}")
            if not result.stdout and not result.stderr:
                output.append("No output produced")
            if result.stdout:
                output.append(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                output.append(f"STDERR:\n{result.stderr}")
            return "\n".join(output)


        except Exception as e:
            return f'Error: reading file "{file_path}": {e}'

import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes text content to a specified file within the working directory (overwriting if the file exists)",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to write, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Text content to write to the file",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
        is_outside_of_working_directory = os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir

        if is_outside_of_working_directory:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
                    
        if os.path.isdir(abs_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # Create directories first
        os.makedirs(abs_working_dir, exist_ok=True)

        # Open and write to file
        with open(abs_file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    
    except Exception as e:
        return f'Error: reading file "{file_path}": {e}'

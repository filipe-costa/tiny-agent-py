import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists the immediate files and subdirectories in a directory within the permitted working directory, printing each entry's name, size in bytes, and whether it is a directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Path to the directory to list, relative to the working directory. The resolved path must remain within the working directory. Omit or use '.' to list the working directory itself.",
                    "default": ".",
                },
            }
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        print(f"Result for {directory} directory:")
        
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            print(f'   Error: Cannot list "{directory}" as it is outside the permitted working directory')
            return

        if not os.path.isdir(target_dir):
            print(f'   Error: "{directory}" is not a directory')
            return

        contents = os.listdir(target_dir)
        res: list[str] = []
        for v in contents:
            path = f"{target_dir}/{v}"
            res.append(f"   - {v}: file_size={os.path.getsize(path)}, is_dir={os.path.isdir(path)}")

        output = "\n".join(res)
        return output
    except Exception as e:
        return f"Error: {e}"

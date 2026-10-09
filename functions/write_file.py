import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
        try:
            print("Working directory:", working_directory)
            print("file_path:", file_path)
            working_dir_abs = os.path.abspath(working_directory)
            # working_dir_abs = os.path.join(abs_dir, working_directory)
            target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))

            # Will be True or False
            valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

            if not valid_target_dir:
                return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
            
            if os.path.isdir(target_dir):
                return f'Error: Cannot write to "{file_path}" as it is a directory'
            
            os.makedirs(os.path.dirname(target_dir), exist_ok=True)

            print("working dir abs", working_dir_abs)
            print("taret dir", target_dir)
            # read file content
            with open(target_dir, "w") as f:
                f.write(content)

            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except Exception as e:
                return f"Error: {e}"

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes or overwrites a file relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Path of the file to write, relative to the working directory"},
                "content": {"type": "string", "description": "The text content to write to the file"},
            },
            "required": ["file_path","content" ],
        },
    },
}
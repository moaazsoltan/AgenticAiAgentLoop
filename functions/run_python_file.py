import os 
import subprocess
import sys
def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
        try:
            working_dir_abs = os.path.abspath(working_directory)
            # working_dir_abs = os.path.join(abs_dir, working_directory)
            target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))

            # Will be True or False
            valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

            if not valid_target_dir:
                return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            
            if not os.path.isfile(target_dir):
                return f'Error: "{file_path}" does not exist or is not a regular file'

            if not target_dir.endswith(".py"):
                return f'Error: "{file_path}" is not a Python file'

            command = ["python", target_dir]

            if args:
                command.extend(args)
            completed_process = subprocess.run(command, 
                                                capture_output=True, 
                                                text=True, 
                                                timeout=30,
                                                cwd=working_dir_abs)
            if not completed_process.returncode == 0:
                return f"Process exited with Code {completed_process.returncode}"

            if completed_process.stderr == "" and completed_process.stdout == "":
                return "No output produced."

            return_value = f"STDOUT: {completed_process.stdout} STDERR:{completed_process.stderr}"

            return return_value
    
        except Exception as e:
            return f"Error: executing Python file: {e}"



schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file within the working directory and returns its stdout, stderr, and exit code",
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
                    "description": "Optional command-line arguments to pass to the script",
                },
            },
            "required": ["file_path"],
        },
    },
}
import os
import subprocess
from google.genai import types

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        # validate that the path to the directory is inside the working_directory
        working_dir_abs = os.path.abspath(working_directory)

        # construct the full file path
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # checks if the target path is within the absolute working directory
        valid_target_path = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
    
        # if the above check returns False
        if valid_target_path is False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
        # checks if the file path points to an existing directory or not
        elif os.path.isfile(target_path) is False:
            return f'Error: "{file_path}" does not exist or is not a regular file'
    
        # checks if the file ends in .py
        elif file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'

        # builds command
        command = ["python", target_path]
        if args:
            command.extend(args)
        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30
        )
        output_list = []
        if result.returncode != 0:
            output_list.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            output_list.append(f"No output produced")
        if result.stdout:
            output_list.append(f"STDOUT: {result.stdout}")
        if result.stderr:
            output_list.append(f"STDERR: {result.stderr}")
        return "\n".join(output_list)

    except Exception as e:
        return f"Error: executing Python file: {e}"
    


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file relative to the working directory, returning a message string",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                        type=types.Type.STRING,
                        description="one command-line argument",
                ),
                description="Optional list of arguments to pass to the Python script",
            ),
        },
        required=["file_path"],
    ),
)
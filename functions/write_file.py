import os
from google.genai import types

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        # validate that the path to the directory is inside the working_directory
        working_dir_abs = os.path.abspath(working_directory)

        # construct the full file path
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # checks if the target path is within the absolute working directory
        valid_target_path = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
    
        # if the above check returns False
        if valid_target_path is False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
        # checks if the file path points to an existing directory or not
        elif os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
    
        # checks if the parent directories of file_path exist
        parent_dir = os.path.dirname(target_path)
        os.makedirs(parent_dir, exist_ok=True)

        # main logic
        with open(target_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        

    except Exception as e:
        return f"Error: {e}"
    


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes file content in a specified file relative to the working directory, returning a success message string",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write into the file",
            ),
        },
        required=["file_path", "content"],
    ),
)
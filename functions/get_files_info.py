import os 
from google.genai import types

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        # validate that the path to the directory is inside the working_directory
        working_dir_abs = os.path.abspath(working_directory)

        # construct the full file path
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # checks if the target directory is within the absolute working directory
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    
        # if the above check returns False
        if valid_target_dir is False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
        # checks if directory is an actual directory or not
        elif os.path.isdir(target_dir) is False:
            return f'Error: "{directory}" is not a directory'
    

        # iterate over the items in the target directory (name, file size, directory t/f)
        tar_dir_contents: list = []
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            tar_dir_contents.append(f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}")
        return "\n".join(tar_dir_contents)

    except Exception as e:
        return f"Error: {e}"



schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
import os 
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        # validate that the path to the directory is inside the working_directory
        working_dir_abs = os.path.abspath(working_directory)

        # construct the full file path
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # checks if the target path is within the absolute working directory
        valid_target_path = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
    
        # if the above check returns False
        if valid_target_path is False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
        # checks if directory is an actual directory or not
        elif os.path.isfile(target_path) is False:
            return f'Error: File not found or is not a regular file: "{file_path}"'
    
        # check if the file is larger than the limit
        with open(target_path, "r") as f:
            file_content_str = f.read(MAX_CHARS)
            if f.read(1):
                file_content_str += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_str

    except Exception as e:
        return f"Error: {e}"
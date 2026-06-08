import os 


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
        elif os.path.isdir(directory) is False:
            return f'Error: "{directory}" is not a directory'
    
        return f'Success: "{directory}" is within the working directory'
    except Exception as e:
        return f"Error: {e}"

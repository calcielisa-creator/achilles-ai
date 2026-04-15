import os

def get_files_info(working_directory, directory= "."):
    try:
        absolute_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_path, directory))
        valid_target_dir = os.path.commonpath([absolute_path, target_dir]) == absolute_path
        if valid_target_dir == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir) == False:
            return f'Error: "{directory}" is not a directory'
    
        list_of_contents = os.listdir(target_dir)
        result = []
        for item in list_of_contents:
            file_size = os.path.getsize(os.path.join(target_dir, item))
            is_dir = os.path.isdir(os.path.join(target_dir, item))
            result.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(result)
    except:
        return f"Error: errors raised by standard library functions"
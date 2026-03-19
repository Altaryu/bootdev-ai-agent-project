import os

def get_files_info(working_directory, directory="."):
    output=[]
    try:
        absolute=os.path.abspath(working_directory)
        target=os.path.normpath(os.path.join(absolute, directory))
        valid_target_dir = os.path.commonpath([absolute, target]) == absolute
        if valid_target_dir == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif os.path.isdir(target) == False:
            return f'Error: "{directory}" is not a directory'
        else:
            for item in os.listdir(target):
                filepath=os.path.join(target, item)
                output.append(f"- {filepath}: file_size={os.path.getsize(filepath)} bytes, is_dir={os.path.isdir(filepath)}")
            return "\n".join(output)
    except Exception as e:
        return f"Error listing files: {e}"
    
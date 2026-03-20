import os

def write_file(working_directory, file_path, content):
    try:
        abs_wrdir=os.path.abspath(working_directory)
        abs_flpth=os.path.normpath(os.path.join(abs_wrdir, file_path))
        valid_flpth=os.path.commonpath([abs_wrdir, abs_flpth]) == abs_wrdir
        if valid_flpth == False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif os.path.isdir(abs_flpth):
            return f'Error: Cannot write to "{file_path}"as it is a directory'
        
        parent_dir=os.path.dirname(abs_flpth)
        os.makedirs(parent_dir, exist_ok=True)

        with open(abs_flpth, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

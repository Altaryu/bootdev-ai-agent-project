import os

def get_file_content(working_directory, file_path):
    MAX_CHARS=10000
    try:
        absolute_wrdir=os.path.abspath(working_directory)
        absolute_flpth=os.path.normpath(os.path.join(absolute_wrdir, file_path))
        valid_target_dir = os.path.commonpath([absolute_wrdir, absolute_flpth]) == absolute_wrdir
        if valid_target_dir == False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif os.path.isfile(absolute_flpth) == False:
            return f'Error: "{file_path}" is not found or is not a regular file.'
        else:
            with open(absolute_flpth, "r") as f:
                file_content_string=f.read(MAX_CHARS)
                if f.read(1):
                    file_content_string+=f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string
    except Exception as e:
        return f'Error listing files: {e}'

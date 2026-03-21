import os
from google.genai import types

MAX_CHARS=10000

def get_file_content(working_directory, file_path):
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


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads file contents in a specified directory relative to the working directory, providing the file content truncated to {MAX_CHARS} characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of file to read contents from."
            )
        },
        required=["file_path"]
    ),
)
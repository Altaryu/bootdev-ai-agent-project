import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_wrdir=os.path.abspath(working_directory)
        abs_flpth=os.path.normpath(os.path.join(abs_wrdir, file_path))
        valid_flpth=os.path.commonpath([abs_wrdir, abs_flpth]) == abs_wrdir
        if valid_flpth == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif os.path.isfile(abs_flpth) == False:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        elif ".py" not in file_path:
            return f'Error: "{file_path}" is not a Python file'
        
        command=["python", abs_flpth]
        if args != None:
            command.extend(args)
        result=subprocess.run(
            command,
            cwd=abs_wrdir,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            return f"Process exited with code {result.returncode}"
        elif result.stdout == "" and result.stderr == "":
            return f"No output produced"
        else:
            return f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    except Exception as e:
        return f"Error: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in a specified directory relative to the working directory, providing the output of stdout and stderr as applicable.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of file to execute."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="An optional array of arguments pertaining to the execution of a given Python file (i.e., '3 + 5')."
            )
        },
        required=["file_path"]
    ),
)
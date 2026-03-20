import os
import subprocess

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
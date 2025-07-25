import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):
    try:
        abs_working = os.path.abspath(working_directory)
        abs_path = os.path.abspath(os.path.join(abs_working, file_path))
        if not abs_path.startswith(abs_working):
            return(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
        if not os.path.exists(abs_path):
            return(f'Error: File "{file_path}" not found.')
        if not abs_path.endswith(".py"):
            return(f'Error: "{file_path}" is not a Python file.')

        sub = subprocess.run(
            ["python", abs_path],
            capture_output=True,
            cwd=abs_working,
            timeout=30,
            text=True
        )

        if not sub.stdout and not sub.stderr:
            return("No output produced.")
        result = f"STDOUT:{sub.stdout.strip()}\nSTDERR:{sub.stderr.strip()}"
        if sub.returncode != 0:
            result += f"\nProcess exited with code {sub.returncode}"
        return result
    except Exception as e:
        return(f"Error: executing Python file: {e}")


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="runs a python file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to",
            ),
        },
    ),
)

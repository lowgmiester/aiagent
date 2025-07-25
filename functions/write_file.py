import os
from google.genai import types

def write_file(working_directory, file_path, content):
    abs_working = os.path.abspath(working_directory)
    abs_path = os.path.abspath(os.path.join(abs_working, file_path))
    if not abs_path.startswith(abs_working):
        return(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
    if not os.path.exists(os.path.dirname(abs_path)):
        try:
            os.makedirs(os.path.dirname(abs_path))
        except Exception:
            return(f'Error: File path not found or does not exist.')
    with open(abs_path, "w") as f:
        f.write(content)
    return(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="writes a file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file"
            ),
        },
    ),
)

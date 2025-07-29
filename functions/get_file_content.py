import os
from .config import *
from google.genai import types

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    can_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not can_path.startswith(abs_working_dir):
        return {"error": f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'}
    if not os.path.isfile(can_path):
        return {"error": f'Error: File not found or is not a regular file: "{file_path}"'}
    try:
        with open(can_path, "r") as f:
            file_content_string = f.read(MAX_CHARS + 1)
            if len(file_content_string) > MAX_CHARS:
                truncated = file_content_string[:MAX_CHARS] + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                return {"content": truncated}
            else:
                return {"content": file_content_string}
    except Exception as e:
        return(f"Error: {str(e)}")

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists the contents of files in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read",
            ),
        },
    ),
)

import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    if directory is None:
        directory = "."
    joined_path = os.path.join(working_directory, directory)
    abs_working = os.path.abspath(working_directory)
    abs_joined = os.path.abspath(joined_path)
    if not abs_joined.startswith(abs_working):
        return(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    if not os.path.isdir(abs_joined):
        return(f'Error: "{directory}" is not a directory')
    info = []
    try:
        for item in os.listdir(abs_joined):
            full_item_path = os.path.join(abs_joined, item)
            size = os.path.getsize(full_item_path)
            string_item = (f" - {item}: file_size={size} bytes, is_dir={os.path.isdir(full_item_path)}")
            info.append(string_item)
        return("\n".join(info))
    except Exception:
        return(f"Error: could not list contents the directory. try again")

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)





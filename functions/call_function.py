from google.genai import types
from .get_files_info import get_files_info
from .get_file_content import get_file_content
from .run_python import run_python_file
from .write_file import write_file

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    name = function_call_part.name
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file
    }

    if name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name,
                    response={"error": f"Unknown function: {name}"},
                )
            ],
        )
    new_args = function_call_part.args.copy()
    new_args["working_directory"] = "./calculator"
    the_function = function_map[name]
    result = the_function(**new_args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=name,
                response=result,
            )
        ],
    )


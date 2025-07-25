import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import *
from functions.get_file_content import *
from functions.run_python import *
from functions.write_file import *
from functions.call_function import call_function


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    user_prompt = sys.argv[1]
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    def ask_llm(messages):
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            )
        )
        for can in response.candidates:
            messages.append(can.content)
        return response

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    if len(sys.argv) < 2:
        print("Error: no prompt provided!")
        sys.exit(1)
    else:
        iterations = 0
        verbose = "--verbose" in sys.argv
        while iterations <= 20:
            try:
                response = ask_llm(messages)
                print("DEBUG: response.function_calls =", getattr(response, "function_calls", None))
                for idx, can in enumerate(getattr(response, "candidates", [])):
                    print(f"DEBUG: candidate[{idx}] function_call =", getattr(can, "function_call", None))
                if response.text:
                    print(response.text)
                    break

                while response.function_calls:
                    for function_call_part in response.function_calls:
                        print(f" - Calling function: {function_call_part.name}")
                        function_call_result = call_function(function_call_part, verbose=verbose)
                        if not function_call_result.parts[0].function_response.response:
                            raise Exception("Error: Function call did not return a valid response")
                        messages.append(function_call_result)
                        print("DEBUG: Tool message appended:", function_call_result)
                        if verbose:
                            print(f"-> {function_call_result.parts[0].function_response.response}")
                    try:
                        response = ask_llm(messages)
                    except Exception as e:
                        print(f"Error: could not generate content. {e}")
                        break
                if response.text:
                    print(response.text)
                    break

            except Exception as e:
                print(f"Error: could not generate content. {e}")
                break

            iterations += 1

        if verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")



if __name__ == "__main__":
    main()

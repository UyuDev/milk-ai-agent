import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function
from config import LOOP_LIMIT
import argparse


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("The api_key is missing. Please check if it was entered correctly.")
    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # the messages list
    messages: list[types.Content] = [
    types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]

    # model calling logic below - implement the loop
    # LOOP_LIMIT is imported from config.py, set to 20
    for _ in range(LOOP_LIMIT):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
        )
        # check the response.candidates property
        if response.candidates:
            for item in response.candidates:
                messages.append(item.content)
        if response.usage_metadata is None:
            raise RuntimeError("Usage metadata not found - likely a failed API request.")
        if response.function_calls is not None:
            function_results = []
            for item in response.function_calls:
                # function_call_result is a types.functioncall object
                function_call_result = call_function(item)
                if not function_call_result.parts:
                    raise Exception("No parts in function call result")
                elif function_call_result.parts[0].function_response is None:
                    raise Exception("No function response stored")
                elif function_call_result.parts[0].function_response.response is None:
                    raise Exception("No function response")
                function_results.append(function_call_result.parts[0])
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=function_results))
    
        else:
            if args.verbose:
                print(
                    f"User prompt: {args.user_prompt}\n"
                    f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n"
                    f"Response tokens: {response.usage_metadata.candidates_token_count}"
                )    
            print(f"Response:\n{response.text}")
            break
    # all iterations were exhausted
    else:
        print("Maximum iterations reached")
        sys.exit(1)


if __name__ == "__main__":
    main()

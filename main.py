import os 
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("The api_key is missing. Please check if it was entered correctly.")
    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
    messages: list[types.Content] = [
    types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
    )
    if response.usage_metadata is None:
        raise RuntimeError("Usage metadata not found - likely a failed API request.")
    print(
        f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n"
        f"Response tokens: {response.usage_metadata.candidates_token_count}"
    )
    print(f"Response:\n{response.text}") 



if __name__ == "__main__":
    main()

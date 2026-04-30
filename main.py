import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    parser = argparse.ArgumentParser(description="achilles-ai")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Environment variable NOT FOUND")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")
    
    generate_content(client, messages, args.verbose)

def generate_content(client, messages, verbose):
    function_results = []
    response = client.models.generate_content(model = "gemini-2.5-flash", contents = messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt, temperature=0),)
    
    if not response.usage_metadata:
        raise RuntimeError("FAILED API request")
    
    if verbose:
        print("Prompt tokens: ", response.usage_metadata.prompt_token_count)
        print("Response tokens: ", response.usage_metadata.candidates_token_count)

    if not response.function_calls:
        print("Response:")
        print(response.text)
        return

    for function_call in response.function_calls:

        function_call_result = call_function(function_call, verbose)

        if not function_call_result.parts:
            raise Exception(f"No function response for {function_call.name}")

        if not function_call_result.parts[0].function_response:
            raise Exception(f"No function response for {function_call.name}")
        
        if not function_call_result.parts[0].function_response.response:
            raise Exception(f"No function response for {function_call.name}")
    
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        
        function_results.append(function_call_result.parts[0])

if __name__ == "__main__":
    main()

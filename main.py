import os
from dotenv import load_dotenv
from google import genai
import argparse

def main():
    print("Hello from achilles-ai!")

    parser = argparse.ArgumentParser(description="achilles-ai")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Environment variable NOT FOUND")

    client = genai.Client(api_key=api_key)

    model = "gemini-2.5-flash"
    contents= args.user_prompt
    
    response = client.models.generate_content(model = model, contents = contents)
    
    if not response.usage_metadata:
        raise RuntimeError("FAILED API request")
    
    print("Prompt tokens: ", response.usage_metadata.prompt_token_count)
    print("Response tokens: ", response.usage_metadata.candidates_token_count)
    print("Response:")
    print(response.text)

if __name__ == "__main__":
    main()

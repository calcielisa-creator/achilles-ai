import os
from dotenv import load_dotenv
from google import genai


def main():
    print("Hello from achilles-ai!")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("Environment variable NOT FOUND")

    client = genai.Client(api_key=api_key)

    contents= "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    model = "gemini-2.5-flash"
    response = client.models.generate_content(model = model, contents = contents)
    print(response.text)
if __name__ == "__main__":
    main()

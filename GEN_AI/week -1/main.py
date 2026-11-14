import os
from dotenv import load_dotenv
from google import genai
from google.genai import errors

# Load the API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY was not found in your .env file.")

client = genai.Client(api_key=api_key)

prompt = "What is Artificial Intelligence? Explain in simple words."

models_to_try = [
    "gemini-3.5-flash",
    "gemini-2.5-flash-lite",
]

for model_name in models_to_try:
    try:
        print(f"Trying {model_name}...")
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )
        print("\nResponse:\n")
        print(response.text)
        break

    except errors.APIError as error:
        print(f"{model_name} failed: {error}")

else:
    print(
        "\nBoth models failed. Try again later, "
        "or check your Gemini API quota and service status."
    )
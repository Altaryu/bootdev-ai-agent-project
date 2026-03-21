import os
import argparse
from prompt import system_prompt
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key=os.environ.get("GEMINI_API_KEY")

if api_key == None:
    raise RuntimeError("no api key was found")

parser=argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args=parser.parse_args()

model_name="gemini-2.5-flash"
messages=[types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

client=genai.Client(api_key=api_key) 
response=client.models.generate_content(
    model=model_name,
contents=messages,
config=types.GenerateContentConfig(system_instruction=system_prompt, temperature=0)
)
if response.usage_metadata != None and args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Response: {response.text}")
elif response.usage_metadata != None and args.verbose == False:
    print(response.text)
else:
    raise RuntimeError("no usage detected")

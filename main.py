import os
import argparse
from prompt import system_prompt
from call_function import available_functions, call_function
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
function_results=[]

client=genai.Client(api_key=api_key) 
response=client.models.generate_content(
    model=model_name,
contents=messages,
config=types.GenerateContentConfig(
    tools=[available_functions],
    system_instruction=system_prompt, 
    temperature=0)
)
if response.usage_metadata != None and args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Response: {response.text}")
    if response.function_calls != None:
        for function in response.function_calls:
            print(f"Calling function: {function.name} ({function.args})")
            call_function_result=call_function(function, args.verbose)
            if call_function_result.parts == []:
                raise Exception("parts should not be empty")
            else:
                if call_function_result.parts[0].function_response == None:
                    raise Exception("parts[0] should not be None")
                elif call_function_result.parts[0].function_response.response == None:
                    raise Exception("response should not be None")
                else:
                    function_results.append(call_function_result.parts[0])
                    print(f"-> {call_function_result.parts[0].function_response.response}")
    


elif response.usage_metadata != None and args.verbose == False:
    print(response.text)
    if response.function_calls != None:
        for function in response.function_calls:
            print(f"Calling function: {function.name} ({function.args})")
            #call_function_result=call_function(function, args.verbose)
            #if call_function_result.types.Content.parts == []:
            #    raise Exception("parts should not be empty")
            #else:
            #    if call_function_result.parts[0].function_response == None:
            #        raise Exception("parts[0] should not be None")
            #    elif call_function_result.parts[0].function_response.response == None:
            #        raise Exception("response should not be None")
            #    else:
            #        function_results.append(call_function_result.parts[0])
            #        print(f"-> {call_function_result.parts[0].function_response.response}")
else:
    raise RuntimeError("no usage detected")

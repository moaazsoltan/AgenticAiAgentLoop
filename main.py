import json
import os
import argparse
from openai import OpenAI
from dotenv import load_dotenv
from prompts import system_prompt
from functions.call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

if api_key is None:
    raise Exception("Runetime Error")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]
for _ in range(20):

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature = 0, 
        tools = available_functions
    )

    result_message = None
    message = response.choices[0].message
    messages.append(message)

    tool_calls = response.choices[0].message.tool_calls
    if tool_calls:
        for tool_call in tool_calls:
            result_message = call_function(tool_call=tool_call, verbose = args.verbose)
            if result_message['content'] == "":
                raise Exception("Empty content")
            if args.verbose and result_message['content'] != None:
                print(f"-> {result_message['content']}")
            messages.append(result_message)
    else:
        break



    # verbosity
    print(response.choices[0].message.content)
    if args.verbose:
        print("User prompt:", args.user_prompt)
        print("Prompt tokens:", response.usage.completion_tokens)
        print("Response tokens:", response.usage.prompt_tokens)

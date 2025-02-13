import sys
import os
from openai import OpenAI
from dotenv import load_dotenv

# ? Custom FC
from actions import get_response_time
from prompts import system_prompt

#sys.path.append(os.path.abspath("../../utils"))
from utils.json_extractor import extract_json


# Load environment variables
load_dotenv()

# Create an instance of the OpenAI class
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_text_with_conversation(messages, model="gpt-3.5-turbo"):
    response = openai_client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content

# First, we define the available functions for this ai agents
available_actions = {
    "get_response_time": get_response_time
}

# Define the prompt
user_prompt = "What is the response time of https://www.youtube.com?"

# Messages to send to the model
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt}
]

# Create a loop to keep the conversation going
turn_count = 1
max_turns = 5

while turn_count < max_turns:
    print(f"Loop: {turn_count}")
    print("--------------------")
    turn_count += 1

    response = generate_text_with_conversation(messages, model="gpt-3.5-turbo")
    print(response)
    json_function = extract_json(response) # - Our model will respond with a json format in order we can extract the data easily

    if json_function:
        function_name = json_function[0]['function_name']
        function_params = json_function[0]['function_params']

        if function_name not in available_actions:
            raise Exception(f"Unknown action: {function_name}: {function_params}")
        print(f" -- running {function_name} {function_params}")
        action_function = available_actions[function_name]
        # call the function
        result = action_function(**function_params)
        function_result_message = f"Action_Response: {result}"
        messages.append({"role": "user", "content": function_result_message})
        print(function_result_message)
    else:
        break
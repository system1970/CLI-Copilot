import os
import openai
import json
import platform

def set_api_key(api_key):
    openai.api_key = api_key

def load_context():
    context_list = ["""
    only reply in this format
    Format:
        1. If the reply contains a command.
        {
            "response_type": 0,
            "command": (The command),
            "did": (A simple, short explanation of what the code did),
            "does": (A simple, short explanation of what the code does),
        }
        2. If the reply does not contain a command
        {
            "response_type": 1,
            "output": (the reply)
        }
    """
    ]
    # with open("context.txt", "r") as context_file:
    #     context_list.append(context_file.read())
    return context_list

def chat_with_gpt3(context_list, behavior_string):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": behavior_string.replace("operating_system", platform.system())},
        ] + [{"role": "user", "content": i} for i in context_list]
    )
    return completion

def main():
    # Set your OpenAI API key
    api_key = input("Enter OpenAI API key: ")
    set_api_key(api_key)

    # Initialize the context
    context_list = load_context()

    # Define the system behavior prompt
    # with open("system_behavior_prompt.txt", "r") as f:
    #     behavior_string = f.read()
    behaviour_string = """You are a chatbot on operating_system that understands and executes command-line operations that gives commands that works on operating_system.
for delete and create commands ask for the filename is the filename is not given."""

    while True:
        user_input = input(">>> ")

        # Add user input to the context
        context_list.append(user_input.rstrip())

        # Use GPT-3.5 for chat completion
        completion = chat_with_gpt3(context_list, behavior_string)

        try:
            reply_message = json.loads(completion.choices[0].message["content"])
            print(reply_message)

            if int(reply_message["response_type"]) == 0:
                while True:
                    state = input("Execute Command (Y/N): ")
                    if state.lower() in ["y", "yes"]:
                        os.system(reply_message["command"])

                        if "cd" in reply_message["command"]:
                            try:
                                os.chdir(reply_message["command"].split(" ")[1])
                                print(os.getcwd())
                                print(reply_message["did"])
                                break
                            except FileNotFoundError:
                                print(reply_message["command"].split(" ")[1] + " does not exist")
                                break
                            except IndexError:
                                break
                        else:
                            print(reply_message["did"])
                            break
                    elif state.lower() in ["n", "no"]:
                        print("Operation cancelled.")
                        break
            else:
                print(reply_message["output"])
        except json.JSONDecodeError:
            reply_message = completion.choices[0].message["content"]
            print(reply_message)

if __name__ == "__main__":
    main()

# TODO: Error handling (eh... mm)
# TODO: Code cleanup (Done)
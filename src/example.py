# A simple example to show how to use the agency

from zhipuai import ZhipuAI
from agency import Agency
    
import os
import tempfile
import subprocess

messages = []

def add_message(role, content):
    messages.append({"role": role, "content": content})

def get_response():
    client = ZhipuAI(api_key='4d050a2bb0eaf43c93b1f205acc3df5d.dW1Oa7aLqq1MgTm4')
    response = client.chat.completions.create(
        model="glm-4",
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content


def run(code):
    code = code[0]
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            # Wrap the code to capture its result
            wrapped_code = f"""
import random
result = eval('''{code}''')
print(result)
"""
            temp_file.write(wrapped_code)
            temp_file_path = temp_file.name

        # Run the temporary file and capture the output
        result = subprocess.check_output(['python', temp_file_path], stderr=subprocess.STDOUT, universal_newlines=True)

        # Return the result
        return result.strip()

    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.strip()}"
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        # Delete the temporary file
        if 'temp_file_path' in locals():
            os.remove(temp_file_path)

info = {"name": "Jack", "age": 20, "problem": "headache"}
def getInfo(code):
    if not (code in info):
        return "No information found"
    return info[code]

num = 71
def guess(numGuessed):
    if numGuessed > num:
        return "Too Big"
    elif numGuessed < num:
        return "Too Small"
    else:
        return "You Get it!"

agent = Agency(get_response_fn=get_response, add_message=add_message, PROMPT="Guess a number between 1 and 100, call function to check")
# agent.add_agent("run", "1", "run code and return the result, the only module imported is random", run)
# agent.add_agent("getInfo", "1", "get the information of the user, the only thing you can pass in is either name, age or problem", getInfo)
agent.add_agent("guess", "1", "guess a number and it'll tell you it's correct, too big or too small, pass the parameter as a number", guess)
response = agent.get_response_new("Hello")
print(response)

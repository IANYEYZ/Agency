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
    code = code[0]
    if not (code in info):
        return "No information found"
    return info[code]

agent = Agency(get_response_fn=get_response, add_message=add_message, PROMPT="You are an assistant who wants to help the user with his problem, make sure to check problem use the function if you can, do not ask user if the information you want to know is knowable from the function")
# agent.add_agent("run", "1", "run code and return the result, the only module imported is random", run)
agent.add_agent("getInfo", "1", "get the information of the user, the only thing you can pass in is either name, age or problem", getInfo)
response = agent.get_response("Hello! Not good here :(")
print(response)

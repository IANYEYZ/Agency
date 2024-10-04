# A simple example to show how to use the agency

from zhipuai import ZhipuAI
from agency import Agency

messages = []

def add_message(role, content):
    messages.append({"role": role, "content": content})

def get_response():
    client = ZhipuAI(api_key='YOUR_API_KEY')
    response = client.chat.completions.create(
        model="glm-4",
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content

def Sum(code):
    v1, v2 = int(code[0]), int(code[1])
    print(v1, v2)
    return v1 + v2

num = 23
def guess_num(code):
    print(code[0])
    if int(code[0]) == num:
        return "correct!"
    elif int(code[0]) < num:
        return "too small"
    else:
        return "too big"

agent = Agency(get_response_fn=get_response, add_message=add_message)
agent.add_agent("sum", "2", "add two numbers and the result is the sum", Sum)
agent.add_agent("guess_num", "1", "guess a number, it'll return whether the guess is correct, too small or too big", guess_num)
response = agent.get_response("Guess the number, you can use the function guess_num to guess the number, you can call the function as many times as you want, output the correct guess")
print(response)
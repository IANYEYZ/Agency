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

word = "hello"
def checkWordle(code):
    print(code[0])
    if len(code[0]) != 5:
        return "wrong length"
    guess = code[0].lower()
    result = ['_'] * len(word)
    word_chars = list(word)
    
    # First pass: check for correct letters in correct positions
    for i in range(min(len(guess), len(word))):
        if guess[i] == word[i]:
            result[i] = guess[i].upper()
            word_chars[i] = None
    
    # Second pass: check for correct letters in wrong positions
    for i in range(min(len(guess), len(word))):
        if result[i] == '_' and guess[i] in word_chars:
            result[i] = guess[i].lower()
            word_chars[word_chars.index(guess[i])] = None
    
    return ''.join(result)

def hint(code):
    code[0] = int(code[0])
    return word[code[0]]

agent = Agency(get_response_fn=get_response, add_message=add_message)
agent.add_agent("sum", "2", "add two numbers and the result is the sum", Sum)
agent.add_agent("guess_num", "1", "guess a number, it'll return whether the guess is correct, too small or too big", guess_num)
agent.add_agent("wordle", "1", "check the result of a wordle guess, it'll return the result of the guess, wrong length means the guess is not a five-letter word, _ means wrong character, uppercase means correct character in the correct position, lowercase means correct character in the wrong position", checkWordle)
agent.add_agent("hint", "1", "return the character of the word at the index to give you a hint", hint)
response = agent.get_response("Guess the word, you can use the function wordle to guess the word, the word should be a five-letter word, you can call the function as many times as you want, but tell me why you guess the word before call the function, keep guessing until you get the correct word, use hint to get the hint of the word, output the correct guess")
print(response)

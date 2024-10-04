# Agency

Agency is a open-source tool to give your text based Large Language Model the ability to use agent.

## Usage

1. Define a function to handle the agent's response, the name, parameter count and description is used to define the agent, and the function is the agent itself, a function for an agent should have only one parameter, which is the argument list of the agent, e,g,:

```python
def Sum(args):
    v1, v2 = int(args[0]), int(args[1])
    return v1 + v2
```

2. Add the agent to the agency

```python
agent = Agency(get_response_fn=get_response, add_message=add_message)  # You can find more information for how to initialize the agency in example.py
agent.add_agent("sum", "2", "add two numbers and the result is the sum", Sum) # description is showed to the LLM to help it understand the agent
```

3. Get the response from the agency

```python
response = agent.get_response("Give me the sum of 1 and 1")
print(response)
```




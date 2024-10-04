class Agency:
    def __init__(self, get_response_fn, add_message):
        prompt = ""
        with open("src/prompt") as f:
            prompt = f.read()
        self.get_response_fn = get_response_fn
        self.add_message = add_message
        self.agents = []
        self.add_message("system", prompt)
    
    def add_agent(self, name, cnt, usage, handler):
        message = f"define {name} {cnt} {usage}"
        self.add_message("user", message)
        self.add_message("assistant", "OK")
        self.agents.append({"name": name, "cnt": cnt, "usage": usage, "handler": handler})

    def get_response(self, message):
        self.add_message("user", message)
        res = self.get_response_fn()
        self.add_message("assistant", res)
        if res.strip().startswith("call"):
            function_name = res.strip().split("(")[0].split("call ")[1]
            for agent in self.agents:
                if agent["name"] == function_name:
                    args = []
                    current_arg = ""
                    parentheses_count = 0
                    for char in res.strip().split("(", 1)[1]:
                        if char == '(':
                            parentheses_count += 1
                            current_arg += char
                        elif char == ')':
                            if parentheses_count == 0:
                                break
                            parentheses_count -= 1
                            current_arg += char
                        elif char == ',' and parentheses_count == 0:
                            args.append(current_arg.strip())
                            current_arg = ""
                        else:
                            current_arg += char
                    if current_arg:
                        args.append(current_arg.strip())
                    return self.get_response(f"RESULT: {agent['handler'](args)}")
        return res
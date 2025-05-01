import re

class Agency:
    def __init__(self, get_response_fn, add_message, PROMPT = ""):
        prompt = ""
        with open("prompt") as f:
            prompt = f.read()
        prompt = prompt.replace("{PROMPT}", PROMPT)
        # print(prompt)
        self.get_response_fn = get_response_fn
        self.add_message = add_message
        self.agents = []
        self.add_message("system", prompt)
        self.context = {}
    
    def add_agent(self, name, cnt, usage, handler):
        message = f"define {name} {cnt} {usage}"
        self.add_message("user", message)
        self.add_message("assistant", "OK")
        self.agents.append({"name": name, "cnt": cnt, "usage": usage, "handler": handler})
        self.context.update({
            name: handler
        })

    def get_response(self, message):
        self.add_message("user", message)
        res = self.get_response_fn()
        self.add_message("assistant", res)
        for agent in self.agents:
            call_string = f"{{{{{agent['name']}("
            for line in res.split('\n'):
                if line.strip().startswith(call_string):
                    args = []
                    current_arg = ""
                    for next_line in res.split('\n')[res.split('\n').index(line)+1:]:
                        if next_line.strip() == ')':
                            if current_arg:
                                args.append(current_arg.strip())
                            break
                        elif next_line.strip() == ',':
                            if current_arg:
                                args.append(current_arg.strip())
                                current_arg = ""
                        else:
                            current_arg += next_line + "\n"
                    function_call_info = f"{agent['name']}({', '.join(args)})"
                    pre_call_content = res[:res.index(line)].strip()
                    pre_call_content += f"\n{function_call_info}\n"
                    res = f"RESULT: {agent['handler'](args)}"
                    pre_call_content += res + "\n"
                    return pre_call_content + self.get_response(res)
        return res
    def get_response_new(self, message):
        self.add_message("user", message)
        res = self.get_response_fn()
        # print(res)
        self.add_message("assistant", res)
        obj = re.search("\{\{.*?\}\}", res)
        if obj == None:
            return res
        # call = res[obj.span()[0] + 2:obj.span()[1] - 2]
        call = obj.group()
        preCall = res[:obj.start()]
        # print(call)
        res = exec(f"res = {call[2:-2]}", self.context, self.context)
        res = self.context["res"]
        del self.context["res"]
        # print(res)
        preCall += f"\n{call}\n"
        res = f"RESULT: {res}"
        return f"{preCall}{res}\n" + self.get_response_new(res)

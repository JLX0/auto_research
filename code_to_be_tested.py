from openai import OpenAI


# shiiiiiit
class gpt:
    def __init__(self, api_key, model="gpt-4o-mini", debug=False):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.debug = debug

        @staticmethod
        def print_prompt(message):
            for prompt_segment in message:
                print(prompt_segment["content"])

    def ask(self, message):
        if self.debug:
            print("-----Prompt beginning marker-----")
            self.print_prompt(message)
            print("-----Prompt ending marker-----")
        response = self.client.chat.completions.create(model=self.model, messages=message)
        response = response.choices[0].message.content
        if self.debug:
            print("------Response beginning marker-----")
            print(response)
            print("------Response ending marker-----")
        return response


# test
# message = [
#     {"role": "system", "content": "Hello"},
# ]
# gpt_instance=gpt("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")
# print(gpt_instance.ask(message))

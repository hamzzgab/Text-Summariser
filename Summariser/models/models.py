import openai
from Summariser.config import Config


class ChatGPTSummariser:
    def __init__(self, prompt, text):
        self.prompt = prompt
        self.text = text
        openai.api_key = Config.KEY

    def get_response(self, model="gpt-3.5-turbo"):
        messages = [{"role": "user",
                     "content": self.prompt + '\n' + self.text}]

        response = openai.ChatCompletion.create(model=model,
                                                messages=messages,
                                                temperature=0)

        return response.choices[0].message["content"]


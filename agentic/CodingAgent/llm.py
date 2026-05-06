import anthropic

class LLMClient:
    def __init__(self, model="claude-sonnet-4-20250514", system_prompt=""):
        self.model = model
        self.system_prompt = system_prompt
        self.max_tokens = 4096
        self.client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

    def chat(self, messages):
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=self.system_prompt,
            messages=messages
        )
        return response.content[0].text
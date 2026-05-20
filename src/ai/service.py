from openai import AsyncOpenAI


class AiService:
    def __init__(self, client: AsyncOpenAI):
        
        self.client = client
        self.model = 'openai/gpt-oss-20b:free'
        
    async def ask_llm(self, messages):
        response = await self.client.chat.completions.create(
          model="openai/gpt-oss-120b:free",
          messages=messages,
          extra_body={"reasoning": {"enabled": True}}
        )

        response = response.choices[0].message
        return response.content




# commits = list[]
# llm -> for commit -> summary commit
# create next logical task based on last commit
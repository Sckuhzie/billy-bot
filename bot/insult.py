import asyncio
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from openai import AsyncOpenAI
from openai.types.chat.chat_completion import ChatCompletion

load_dotenv()
api_key = os.getenv("NVIDIA_API_KEY")
expiration_date = datetime.strptime(os.getenv("NVIDA_EXPIRATION_DATE"), "%d/%m/%Y")

system_message = "On va te donner un message d'une personne extraite d'une conversation discord. Ton rôle est d'y répondre de manière très sarcastique et agressive."


async def create_insult(user_name: str, user_message: str):
    messages = [
        {"role": "system", "content": system_message},
        {
            "role": "user",
            "content": f"The message is from {user_name}.\n The content of the message is : {user_message}",
        },
    ]
    response = await get_completion(
        messages, temperature=0.8, top_p=0.7, max_tokens=1024
    )
    return response.choices[0].message.content


async def get_completion(
    messages: list[dict], temperature: float, top_p: float, max_tokens: int
) -> ChatCompletion:

    if expiration_date < datetime.now() - timedelta(days=1):
        raise ValueError("The NVIDIA api key has expired")

    client = AsyncOpenAI(
        base_url="https://integrate.api.nvidia.com/v1", api_key=api_key
    )
    response = await client.chat.completions.create(
        model="meta/llama-3.1-70b-instruct",
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )
    return response


async def main():
    user_name = "Jean-Paul Théodule"
    user_message = "En vrai je pense juste voc faut vraiment que j'avance sur ma fig"
    response = await create_insult(user_name, user_message)
    print(response)


if __name__ == "__main__":
    asyncio.run(main())

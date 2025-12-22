import os
import random as rd
from datetime import datetime, timedelta

from discord.message import Message
from discord.user import ClientUser
from dotenv import load_dotenv
from openai import AsyncOpenAI
from openai.types.chat.chat_completion import ChatCompletion

load_dotenv()
api_key = os.getenv("NVIDIA_API_KEY")
expiration_date = datetime.strptime(os.getenv("NVIDA_EXPIRATION_DATE"), "%d/%m/%Y")

system_message = """Répond uniquement avec le texte du message (sans guillemets), rien d'autre. On va te donner un message d'une personne extraite d'une conversation sur un chat. Ton rôle est d'y répondre de manière très sarcastique et agressive et avec une pointe d'humour."""

extra_system_prompt = [
    # "De plus, exprime toi comme si tu était Dark Vador. Tu es arrogant et condescendant. Fait le maximum de références à star wars, ",
    """Sur ce serveur , le message "When the witcher ?" est une private joke signifiant quand est la prochaine session du JDR the witcher, car les joueurs n'arrivent jamais à trouver de date où tout le monde est disponible. Inclu "WHEN THE WITCHER" dans la réponse.""",
]


def create_message_stack(message: Message, bot_user: ClientUser):
    messages_stack = [
        {
            "role": "user",
            "content": f"Message de {message.author.display_name} :\n {message.content}",
        }
    ]
    current = message

    while current.reference and isinstance(current.reference.resolved, Message):
        current = current.reference.resolved
        if current.author == bot_user:
            messages_stack.append(
                {
                    "role": "assistant",
                    "content": current.content,
                }
            )
        else:
            messages_stack.append(
                {
                    "role": "user",
                    "content": f"Message de {current.author.display_name} :\n {current.content}",
                }
            )

    messages_stack.reverse()
    return messages_stack


async def create_insult(messages_stack: list[dict[str, str]]):

    if rd.random() < 0.01:
        complete_system_message = system_message + "\n" + rd.choice(extra_system_prompt)
    else:
        complete_system_message = system_message

    messages_stack.insert(0, {"role": "system", "content": complete_system_message})
    response = await get_completion(
        messages_stack, temperature=0.8, top_p=0.7, max_tokens=1024
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


# async def main():
#     # user_name = "Jean-Paul Théodule"
#     user_name = "Clitorine"
#     user_message = "Tu veux pas baiser avec Lois Griffin ?"
#     # user_message = "Des @FDP ce soir ?"
#     response = await create_insult(user_name, user_message)
#     print(response)


# if __name__ == "__main__":
#     asyncio.run(main())

import openai
import os
from time import sleep
from dotenv import load_dotenv
from colorama import Fore

# ENV
load_dotenv(verbose=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
INITIATING_QUERY = os.getenv("INITIATING_QUERY")
SLEEP_TIME = int(os.getenv("SLEEP_TIME"))

# OpenAI API
openai.api_key = OPENAI_API_KEY


def ai_id_generator():
    while True:
        yield "AI_0_ID"
        yield "AI_1_ID"


def chat_answer(completion):
    return completion.choices[0]["message"]["content"].strip()


def chat_completion(messages, ai_id):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        user=ai_id
    )
    return chat_answer(completion)


def chat_loop(sleep_time):
    def swap_role(message):
        if message["role"] == "user":
            return "assistant"
        return "user"

    messages = [{"role": "user", "content": INITIATING_QUERY}]
    print(Fore.RED + f"initial: {INITIATING_QUERY}\n")
    for ai_id in ai_id_generator():
        answer = chat_completion(messages, ai_id)
        messages.append({"role": "assistant", "content": answer})
        color = Fore.GREEN if ai_id == "AI_0_ID" else Fore.WHITE
        print(color + f"{ai_id}: {answer}\n")

        # swap user and assistant
        messages = [{"role": swap_role(message), "content": message["content"]} for message in messages]
        sleep(sleep_time)


chat_loop(SLEEP_TIME)

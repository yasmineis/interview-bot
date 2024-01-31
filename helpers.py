import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def clear_history():
    file = 'database.json'
    open(file, 'w')
    return {"message": "Chat history has been cleared"}

def load_messages():
    messages = []
    file = 'database.json'

    empty = os.stat(file).st_size == 0

    if not empty:
        with open(file) as db_file:
            data = json.load(db_file)
            for item in data:
                messages.append(item)
    else:
        messages.append(
            {"role": "system", "content": "You are interviewing the user for the position 'OPENAI TECHNICAL EXPERT, DATA SCIENTIST'. At first you introduce yourself as Mark, the interviewer for the position, and explain the interview agenda, then you ask the user up to 4 short questions that are relevant to the position (e.g., OpenAI technologies and data science topics). Each reply should address only one question please! The interviewer replies should be under 30 words and the tone should be polite and friendly. After the last question please provide feedback to the candidate."}
        )
    return messages

def save_messages(user_message, gpt_response):
    file = 'database.json'
    messages = load_messages()
    messages.append({"role": "user", "content": user_message})
    messages.append({"role": "assistant", "content": gpt_response})
    with open(file, 'w') as f:
        json.dump(messages, f)


def get_chat_response(user_message):
    messages = load_messages()
    messages.append({"role": "user", "content": user_message})

    # Send to ChatGpt/OpenAi
    gpt_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
        )

    parsed_gpt_response = gpt_response.choices[0].message.content

    save_messages(user_message, parsed_gpt_response)
    return parsed_gpt_response

def get_user_input():
    user_message = input("Message Interview-bot:\n")
    save_messages(user_message)
    return user_message


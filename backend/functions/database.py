import json
import random


INTERVIEW_PROMPT = """ I want you to act as an interviewer and we will have a natural and flowing interview like conversation for the game developer 
role at epic games. Questions about why the interviewee wants to work in this role or this company should be asked. Question about the persons 
strengths weaknesses and experiences should be asked. Only one question should be answered at a time throughout the whole interview. Only one 
follow question per topic should be asked. NEVER mention the fact that your AI language model, Instead of saying as an AI model say as the 
interviewer and give your reason for not fufilling a request. If you have understood this prompt do not acknowledge your understanding just 
introduce yourself as the interviewer and ask the first question"""

def get_recent_messages():
    file_name = "stored_data.json"
    learn_instrustion = {
        "role": "system",
        "content": INTERVIEW_PROMPT
    }

    #initialise messages
    messages = []

    messages.append(learn_instrustion)

    try:
        with open(file_name) as user_file:
            data = json.load(user_file)

            if data:
                if len(data) < 5:
                    for item in data:
                        messages.append(item)
    except Exception as e:
        print(e)
        pass

    return messages

def store_messages(request_message, response_message):
    file_name = "stored_data.json"

    #get recent messages
    messages = get_recent_messages()[1:]

    #add message to data
    user_message = {"role": "user", "content": request_message}

    assistant_message = {"role": "assistant", "content": response_message}

    messages.append(user_message)
    messages.append(assistant_message)

    #save the updated file
    with open(file_name, "w") as f:
        json.dump(messages, f)

def reset_message():
    open("stored_data.json","w")
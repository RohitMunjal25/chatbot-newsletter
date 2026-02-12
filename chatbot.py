import json

with open("dataset.json") as f:
    DATA = json.load(f)["faq"]

def find_answer(user_msg):
    user_msg = user_msg.strip().lower()

    for item in DATA:
        question = item["question"].strip().lower()

        if user_msg in question or question in user_msg:
            return item["answer"]

    return None

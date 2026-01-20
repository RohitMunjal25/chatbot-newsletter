import json

with open("dataset.json") as f:
    DATA = json.load(f)["faq"]

def find_answer(user_msg):
    user_msg = user_msg.lower()
    for item in DATA:
        if item["question"] in user_msg:
            return item["answer"]
    return None

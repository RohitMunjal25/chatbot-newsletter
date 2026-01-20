import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
MONGO_URL= os.getenv("MONGO_URL")
client=MongoClient(MONGO_URL)
db=client("newsletterDB")
subscribers_col=db["subscribers"]
chatlogs_col=db["chat_logs"]
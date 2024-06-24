from pymongo import MongoClient
from datetime import datetime, timedelta
from dotenv import load_dotenv
import random
import os
# mongodb local
#client = MongoClient('localhost', 27017)

load_dotenv()

# mongodb atlas
client = MongoClient(os.environ.get("MONGO_URI"))
db = client.empty_space_numbers
collection = db.real

from pymongo import MongoClient
from datetime import datetime, timedelta
import random

# mongodb 
client = MongoClient('localhost', 27017)
db = client.flask_db
collection = db.empty_space_numbers

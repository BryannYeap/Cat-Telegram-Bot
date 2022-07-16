from pymongo import MongoClient
import logger
from user_entity import User_Entity
from dotenv import load_dotenv
import os

# Access secret keys saved in .env file (telegram bot token obtained from bot father)
load_dotenv()
CONNECTION_STRING = os.getenv('MONGO_CONNECTION_STRING')
DATABASE = os.getenv('MONGO_DATABASE')
COLLECTION = os.getenv('MONGO_COLLECTION')

client = MongoClient(CONNECTION_STRING)
logger.info("Successfully connected to MongoDB")

users_db = client[DATABASE]
logger.info(f"DATABASE: {users_db}")

users = users_db[COLLECTION]
logger.info(f"COLLECTION: {users}")


def get_all_users():
    return list(map(lambda document : map_document_to_user_entity(document), users.find()))

def user_exists(id):
    x = users.count_documents({"user_id" : str(id)}) != 0
    return x

def get_user(id):
    user_document = users.find_one({"user_id" : str(id)})
    return map_document_to_user_entity(user_document)

def add_user(new_user_entity):
    users.insert_one(new_user_entity.__dict__)

def update_user(id, new_user_entity):
    users.update_many({"user_id" : str(id)}, {"$set": new_user_entity.__dict__})

def delete_user(id):
    users.delete_many({"user_id" : str(id)})

# Util

def map_document_to_user_entity(document):
    try:
        del document['_id']
        return User_Entity(**document)
    except TypeError:
        logger.error("User of given ID not found. Returning None")

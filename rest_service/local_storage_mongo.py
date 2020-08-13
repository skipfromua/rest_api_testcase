from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

local_storage = client.tododb

unloaded_data = local_storage["unloaded_data"]
cached_data = local_storage["cached_data"]

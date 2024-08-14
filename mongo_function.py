import os
import pymongo
from pymongo import MongoClient
from bson import json_util
from hashlib import sha256
import json

from config import host, port, database_name, product_collection_name

def partitionData(databaseName, collectionName, partition_key, base_dir=os.path.join("mongosDir", "partitioned")):
    try:
        base_dir = os.path.join(os.getcwd(), base_dir)
        client = MongoClient(host, port)
        collection = client[databaseName][collectionName]

        os.makedirs(base_dir, exist_ok=True)

        for document in collection.find():
            partition_value = document.get(partition_key)
            partition_dir = os.path.join(base_dir, "unpartitioned" if partition_value is None else str(partition_value))
            os.makedirs(partition_dir, exist_ok=True)

            with open(os.path.join(partition_dir, f"{document['_id']}.json"), "w") as f:
                f.write(json_util.dumps(document))

        return True
    except Exception as e:
        # print(f"Error in partitionData: {e}")
        return False

def shardDataset(database_name, collection_name, shard_key, num_shards=4, base_dir=os.path.join("mongosDir", "sharded")):
    try:
        base_dir = os.path.join(os.getcwd(), base_dir, f"{collection_name}_shards")
        os.makedirs(base_dir, exist_ok=True)

        client = MongoClient(host, port)
        collection = client[database_name][collection_name]

        shards_dirs = [os.path.join(base_dir, f"shard_{i}") for i in range(num_shards)]
        for shard_dir in shards_dirs:
            os.makedirs(shard_dir, exist_ok=True)

        for document in collection.find():
            shard_index = int(sha256(str(document[shard_key]).encode()).hexdigest(), 16) % num_shards
            file_path = os.path.join(shards_dirs[shard_index], f"{document['_id']}.json")
            with open(file_path, 'w') as f:
                f.write(json_util.dumps(document))

        return True
    except Exception as e:
        # print(f"Error in shardDataset: {e}")
        return False



# def shardInMongo(database)
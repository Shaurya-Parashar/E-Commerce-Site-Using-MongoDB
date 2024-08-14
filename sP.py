from pymongo import MongoClient
from config import database_name, product_collection_name, host, port

# Configuration
config = {
    'mongodb_host': host,
    'mongodb_port': port,
    'source_db_name': database_name,
    'source_collection_name': product_collection_name,
    'target_db_base_name': "shardPdb",  # Base name for sharding simulation
    'partition_db_name': 'partition_db',  # Database name for partitioning simulation
}

client = MongoClient(config['mongodb_host'], config['mongodb_port'])


def Sharding(shard_key, num_shards=4):
    source_db = client[config['source_db_name']]
    source_collection = source_db[config['source_collection_name']]

    for document in source_collection.find():
        shard_value = document.get(shard_key)
        if shard_value is None:
            continue  # Skip documents without a shard key

        # Hashing shard_key to determine target shard
        shard_index = hash(shard_value) % num_shards
        target_db_name = f"{config['target_db_base_name']}_shard_{shard_index}"
        target_db = client[target_db_name]
        target_collection = target_db[config['source_collection_name']]

        target_collection.insert_one(document) 


def Partitioning(partition_key):
    source_db = client[config['source_db_name']]
    source_collection = source_db[config['source_collection_name']]
    partition_db = client[config['partition_db_name']]

    for document in source_collection.find():
        partition_value = document.get(partition_key)
        if partition_value is None:
            continue  # Skip documents without a partition key

        # Using partition_value to determine target collection
        target_collection_name = f"partitioned_{partition_value}"
        target_collection = partition_db[target_collection_name]

        target_collection.insert_one(document)

# Simulate sharding
Sharding('Gender', 2)

# Simulate partitioning
# Partitioning('Category')
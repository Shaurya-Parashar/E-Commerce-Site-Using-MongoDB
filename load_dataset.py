import os
import polars as pl
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from config import database_name, product_collection_name, dataset_base_dir, host, port

dataset_base_dir = os.path.join(os.getcwd(), dataset_base_dir)

fashion_path = os.path.join(dataset_base_dir, "fashion.csv")

def loadCSV(path):
    try:
        df = pl.read_csv(path)
        return df
    except Exception as e:
        raise Exception(f"Failed to load CSV: {e}")

def getToMongo(collection, df, base_dir):
    for row in df.to_dicts():
        category = row['Category']
        gen = row['Gender']
        image_file = row['Image']
        full_image_path = os.path.join(base_dir, category,gen, "Images", "images_with_product_ids", image_file)

        row['Image'] = full_image_path

        # Delete key from dictionary
        del row['ImageURL']
        
        try:
            collection.insert_one(row)
        except DuplicateKeyError as e:
            raise DuplicateKeyError(f"Duplicate entry: {e}")
        except Exception as e:
            raise Exception(f"Error inserting document: {e}")

def initMongoDB(databaseName, collectionName, fashionPath, base_dir):
    try:
        client = MongoClient(host, port)
        db = client[databaseName]

        if collectionName in db.list_collection_names():
            return db[collectionName]
        
        collection = db[collectionName]
        df = loadCSV(fashionPath)
        if df is not None:
            getToMongo(collection, df, base_dir)
        else:
            raise Exception("Error loading the dataset.")
        return collection
    
    except Exception as e:
        raise Exception(f"Error initializing MongoDB: {e}")


def getData(collection):
    try:
        data = list(collection.find())
        for i in range(len(data)):
            data[i].pop('_id')
            data[i]['id'] = i
        return data
    except Exception as e:
        raise Exception(f"Error fetching data: {e}")


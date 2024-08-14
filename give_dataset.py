from flask import Flask, request, jsonify, blueprints
from load_dataset import dataset_base_dir, fashion_path, initMongoDB, getData
from config import database_name, product_collection_name
import json

loadDataset = blueprints.Blueprint('loadDataset', __name__)

@loadDataset.route('/getDataset', methods=['GET'])
def load():
    try:
        collection = initMongoDB(database_name, product_collection_name, fashion_path, dataset_base_dir)
        data = getData(collection)

        return jsonify({"status": True, "message": "Data loaded successfully", "data": data})
    except Exception as e:
        return jsonify({"status": False, "message": str(e)})
        
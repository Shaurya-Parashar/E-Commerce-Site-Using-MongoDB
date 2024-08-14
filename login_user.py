from flask import Flask, request, jsonify, blueprints
from database_functionality import createDatabaseAndCollection, insertData, getData, updateData, deleteData, checkPasswordFromEmail
from config import login_collection_name, database_name

loginUser = blueprints.Blueprint('loginUser', __name__)


@loginUser.route('/signup', methods=['POST'])
def signup():
    try:
        
        coll = createDatabaseAndCollection(database_name, login_collection_name)
        data = request.json
        
        firstName = data['firstName']
        lastName = data['lastName']
        phoneNumber = data['phoneNumber']
        email = data['email']
        gender = data['gender']
        address = data['address']
        state = data['state']
        password = data['password']


        insertData(coll, firstName, lastName, phoneNumber, email, gender, address, state, password)
        return jsonify({"status": True, "message": "User added successfully"})
    
    except Exception as e:
        return jsonify({"status": False, "message": str(e)})

@loginUser.route('/login', methods=['POST'])
def login():
    try:
        coll = createDatabaseAndCollection(database_name, login_collection_name)
        data = request.json
        email = data['email']
        password = data['password']
        if checkPasswordFromEmail(coll, email, password):
            return jsonify({"status": True, "message": "Login successful"})
        else:
            return jsonify({"status": False, "message": "Login failed"})
    except Exception as e:
        return jsonify({"status": False, "message": str(e)})

@loginUser.route('/update', methods=['POST'])
def update():
    try:
        coll = createDatabaseAndCollection(database_name, login_collection_name)
        data = request.json
        email = data['email']
        key = data['key']
        value = data['value']
        if updateData(coll, email, key, value):
            return jsonify({"status": True, "message": "Data updated successfully"})
        else:
            return jsonify({"status": False, "message": "Data update failed"})
    except Exception as e:
        return jsonify({"status": False, "message": str(e)})

@loginUser.route('/delete', methods=['POST'])
def delete():
    try:
        coll = createDatabaseAndCollection(database_name, login_collection_name)
        data = request.json
        email = data['email']
        if deleteData(coll, email):
            return jsonify({"status": True, "message": "Data deleted successfully"})
        else:
            return jsonify({"status": False, "message": "Data delete failed"})
    except Exception as e:
        return jsonify({"status": False, "message": str(e)})

@loginUser.route('/get', methods=['POST'])
def get():
    try:
        coll = createDatabaseAndCollection(database_name, login_collection_name)
        data = request.json
        email = data['email']
        data = getData(coll, email)
        firstName = data['firstName']
        lastName = data['lastName']
        phoneNumber = data['phoneNumber']
        gender = data['gender']
        address = data['address']
        state = data['state']

        return jsonify({"status": True, "firstName": firstName, "lastName": lastName, "phoneNumber": phoneNumber, "gender": gender, 'address': address, 'state': state})
    except Exception as e:
        return jsonify({"status": False, "message": str(e)})
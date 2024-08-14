# Connect To MongoDB

from config import host, port
from validateInput import validate_crypt as vc


import pymongo
from pymongo import MongoClient, errors
import bcrypt


# Function to create a database and collection
def createDatabaseAndCollection(databaseName, collectionName):
    try:

        client = MongoClient(host, port)
        db = client[databaseName]
        collection = db[collectionName]
        collection.create_index([('email', pymongo.ASCENDING)], unique=True)
        return collection

    except errors.ConnectionFailure as e:
        raise Exception("Could not connect to MongoDB: %s" % e)

    except Exception as e:
        raise Exception("Error %s" % e)


# Function to insert data into the collection, insert name, email, password, phone number, gender, address, state and password
def insertData(collection, firstName, lastName, phoneNumber, email, gender, address, state, password):
    try:

        if not vc.validate_all(firstName, lastName, phoneNumber, email, gender, address, state, password):
            return False

        # Hash Password
        hashedPassword = vc.cryptPassword(password)

        # Insert Data
        collection.insert_one(
            {
                "firstName": firstName,
                "lastName": lastName,
                "phoneNumber": phoneNumber,
                "email": email,    
                "gender": gender, 
                "address": address,
                "state": state,
                "password": hashedPassword
            })
        
        return True
    
    except errors.DuplicateKeyError as e:
        raise Exception("Email Already Exists: %s" % e)

    except Exception as e:
        raise Exception("Error %s" % e)


# Function to find data in the collection
def getData(collection, email):
    try:

        # Find Data
        data = collection.find_one({"email": email})
        return data
    
    except Exception as e:
        raise Exception("Error %s" % e)


# Function to update data in the collection
def updateData(collection, email, key, value):
    try:
        
        # Validate Key Value
        if not vc.validate_key(key, value):
            return False

        if key == "password":
            value = vc.cryptPassword(value)

        # Update Data
        collection.update_one({"email": email}, {"$set": {key: value}})

        return True
    
    except Exception as e:
        raise Exception("Error %s" % e)


# Function to delete data in the collection
def deleteData(collection, email):
    try:

        # Delete Data
        collection.delete_one({"email": email})
        return True
    
    except Exception as e:
        raise Exception("Error %s" % e)


# Function To Validate Password and Email
def checkPasswordFromEmail(collection, email, password):
    try:
        # Get Data
        data = collection.find_one({"email": email})
        passwordHash = data["password"]

        # Check Password
        if vc.checkPassword(password, passwordHash):
            return True
        return False
    
    except Exception as e:
        raise Exception("Error %s" % e)
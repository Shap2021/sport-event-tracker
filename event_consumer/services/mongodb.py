"""
Controller module for MongoDB
"""
import json
from urllib.parse import quote_plus
from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from core.config import settings

# Mongodb connection string below
# mongodb+srv://<username>:<db_password>@cluster0.rfvytng.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
# don't forget to set the mongodb env credentials!

# I may update the structure of this project to use service logic separte from the main logic
# base file that has the session injection and basic database operations like read and write
# You can use the TypeDict from the typing library to insert records using schema validation

class MongoDBConn:
    def __init__(self):
        # Initialize the mongodb connection here
        self.client = self._connect_to_mongodb()
        self.database = self.client[settings.mongodb_database]
        self.collection = self.database[settings.mongodb_collection]


        # Try to ping the database to make sure the connection worked
        try:
            self.client.admin.command('ping')
            print('Client intialized. You successfully connected to MongoDB!')
        except Exception as err:
            print('Issue connecting to cluster: ', err)

    # internal method to create the connection string with env variables
    def _create_mongodb_uri(self):
        """
        Create mongodb connection uri. The connection string template
        comes from the MongDB Atlas website cloud.mongodb.com.
        """
        return (
            "mongodb+srv://"
            f"{settings.mongodb_username}:{quote_plus(settings.mongodb_password)}"
            f"@{settings.mongodb_cluster}.rfvytng.mongodb.net/"
            f"?retryWrites=true&w=majority&appName={settings.mongodb_cluster}"
        )

    # internal method to actually connect to mongodb that __init__ will call
    def _connect_to_mongodb(self):
        """
        Connect to MongoDB cluster using PyMongo.
        """
        return MongoClient(
            self._create_mongodb_uri(),
            server_api=ServerApi('1')
            )

    # methods to insert data and read data
    def insert_record(self, document:dict):
        """
        Insert one record to collection. 
        """
        # Should add dict validation either with Pydantic, TypeDict, or isinstance
        result = self.collection.insert_one(document,
                                   bypass_document_validation=False)
        return result.inserted_id
        
    def insert_many_records(self, documents:list): # Only lists are allowed
        """
        Insert a list of documents to collection.
        """
        if not isinstance(documents, list):
            raise AttributeError(
                "Documents must be inside a list."
            )
        
        self.collection.insert_many(documents,
                                    bypass_document_validation=False)
    
    def read_record(self, object_id:str):
        """
        Read document from collection using document
        object id.
        """
        return (
            self.collection.find_one({"_id": ObjectId(object_id)})
        )
    
    def shutdown(self):
        """
        Close MongoDB Connection
        """
        self.client.close()

class MongoDataManager(MongoDBConn):
    """
    MongoDB database/document operations
    """
    def add_one_doc(self, payload:dict):
        """
        Add one document to MongDB collection
        """
        record = payload.value()
        return self.insert_record(json.loads(record.decode('utf-8'))) # Will need to update to be sent to a dead letter queue if something failed

    def read_document_by_id(self, object_id:str):
        return self.read_record(object_id=object_id)

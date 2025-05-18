# db.py - Database configuration
import pymongo
import certifi
import os
from bson.objectid import ObjectId

class Database:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Database()
        return cls._instance
    
    def __init__(self):
        """Initialize database connection"""
        try:
            self.client = pymongo.MongoClient(
                os.getenv("CONNECTION_STRING"), 
                tlsCAFile=certifi.where(),
                serverSelectionTimeoutMS=5000  # 5-second timeout
            )
            # Test connection
            self.client.server_info()
            self.db = self.client.get_database("dentixpro")
            print("Connected to MongoDB successfully!")
        except pymongo.errors.ServerSelectionTimeoutError as err:
            print(f"Could not connect to MongoDB: {err}")
            raise
    
    def get_collection(self, collection_name):
        """Get a collection from the database"""
        return self.db[collection_name]
    
    @staticmethod    
    def fix_id(obj):
        """Convert MongoDB ObjectId to string in a single object"""
        if obj and "_id" in obj:
            obj["_id"] = str(obj["_id"])
        return obj
    
    @staticmethod
    def fix_ids(objects):
        """Convert MongoDB ObjectIds to strings in a list of objects"""
        return [Database.fix_id(obj) for obj in objects]
    
    @staticmethod
    def to_object_id(id_str):
        """Convert string ID to MongoDB ObjectId"""
        try:
            return ObjectId(id_str)
        except:
            return None
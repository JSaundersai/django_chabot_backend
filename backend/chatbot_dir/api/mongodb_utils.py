from pymongo import MongoClient
from typing import Tuple
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

def get_db_handle() -> Tuple[MongoClient, MongoClient]:
    """
    Get MongoDB database handle and client
    Returns tuple of (db_handle, client)
    """
    try:
        # Load environment variables
        load_dotenv()
        
        # Get credentials
        username = quote_plus(os.getenv('MONGODB_USERNAME', ''))
        password = quote_plus(os.getenv('MONGODB_PASSWORD', ''))
        cluster = os.getenv('MONGODB_CLUSTER', '')
        database = os.getenv('MONGODB_DATABASE', '')
        
        # Validate credentials
        if not all([username, password, cluster, database]):
            raise ValueError("Missing MongoDB configuration in environment variables")
            
        # Construct connection string
        uri = f"mongodb+srv://{username}:{password}@{cluster}/{database}?retryWrites=true&w=majority"
        
        # Create client with timeouts
        client = MongoClient(uri, 
                           serverSelectionTimeoutMS=5000,
                           connectTimeoutMS=5000)
        
        # Test connection
        client.server_info()
        db_handle = client[database]
        
        return db_handle, client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise

if __name__ == "__main__":
    try:
        db, client = get_db_handle()
        print("Successfully connected to MongoDB!")
        print(f"Database name: {db.name}")
        print(f"Collections: {db.list_collection_names()}")
        client.close()
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
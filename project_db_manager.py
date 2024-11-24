from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class DatabaseManager:
    def __init__(self, db_name, collection_name):
        self.db_name = db_name
        self.collection_name = collection_name
        self.db_connection = self.connect_to_database()

    def connect_to_database(self):
        DB_NAME = self.db_name
        DB_HOST = "localhost"
        DB_PORT = 27017
        try:
            client = MongoClient(host=DB_HOST, port=DB_PORT)
            db = client[DB_NAME]
            return db
        except:
            print("Database did not connect successfully")


    def insert_document_duplicate_accepted(self, doc_obj):
        collection = self.db_connection[self.collection_name]
        result = collection.insert_one(doc_obj)
        return result.inserted_id


    def insert_document(self, doc_obj):
        collection = self.db_connection[self.collection_name]
        try:
            result = collection.insert_one(doc_obj)
            return result.inserted_id
        except DuplicateKeyError:
            print(f"Duplicate entry detected. Skipping insertion.")
            return None


    def get_document_html(self, page_url):
        db_connection = self.connect_to_database()
        collection = db_connection[self.collection_name]
        result = collection.find_one({
            "url": page_url
        })
        return result
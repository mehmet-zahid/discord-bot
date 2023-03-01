from pymongo import MongoClient
from pymongo.results import InsertOneResult, InsertManyResult
import os
from pprint import pprint
from loguru import logger


class MongoManager:
    def __init__(self, db_name, conn_str: str=None):
        self.db_name = db_name
        
        if conn_str is None:
            self.conn_str = os.environ.get("MONGODB_PWD")
            print(self.conn_str)
        else:
            self.conn_str = conn_str
            print(self.conn_str)

        self.client = MongoClient(host=self.conn_str)


    def add_document(self, document: dict, collection_name) -> InsertOneResult:
        
        doc = self.get_collection(collection_name).insert_one(document)
        print(f"Inserted {document}")
        return doc

    def add_documents(self, collection_name, documents: list[dict]) -> InsertManyResult:
        print("Inserted documents")
        docs = self.get_collection(collection_name).insert_many(documents)
        return docs

    def show_all_documents(self, collection_name):
        for item in self.get_collection(collection_name).find():
            pprint(item)

    def get_documents_by_filter(self, item: dict, collection_name):
        docs = []
        for item in self.get_database()[collection_name].find(item):
            docs.append(item)
        pprint(docs)
    
    def get_database_names(self):
        """
        :return: a list of all the database names
        """
        try:
            dbs = self.client.list_database_names()

            logger.info("Database names method was called.")

            return dbs

        except Exception as e:
            logger.error(e)
            return e

    def get_database(self, db_name: str=None):
        """
        :param db_name: the name of the database to get
        :return: the database object
        """
        if self.db_name:
            db_name = self.db_name
        
        try:
            db = self.client[db_name]

            logger.info("Database method was called.")

            return db

        except Exception as e:
            logger.error(e)
            return e

    def get_collections_names(self, db_name: str=None):
        """
        :param db_name: the name of the database to get the collections from
        :return: a list of all the collections in the database
        """
        if self.db_name:
            db_name = self.db_name
        try:
            db = self.get_database(db_name)
            collections = db.list_collection_names()

            logger.info("Collections names method was called.")

            return collections

        except Exception as e:
            logger.error(e)
            return e

    def get_collection(self, collection_name: str, db_name: str=None):
        """
        :param collection_name: the name of the collection to get
        :return: the collection object
        """
        if self.db_name:
            db_name = self.db_name
        try:
            db = self.get_database(db_name)
            collection = db[collection_name]

            logger.info("Collection method was called.")

            return collection

        except Exception as e:
            logger.error(e)
            return e

# import motor.motor_asyncio

#client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get('MONGODB_PWD'))

#DB_NAME = "discord"
#COLLECTION_NAME = "beyaz_klavye"
#TEST_COLLECTION_NAME = "test"
#db = client[DB_NAME]
#collection = db[COLLECTION_NAME]



    

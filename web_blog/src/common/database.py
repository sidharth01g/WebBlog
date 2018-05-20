import pymongo
from typing import Optional, Dict, List


class Database(object):

    def __init__(self, uri: str = 'mongodb://127.0.0.1:27017', db_name: str = None) -> None:
        self.uri = uri
        self.db_name = db_name

        self.client = pymongo.MongoClient(self.uri)
        self.database = self.client[self.db_name]

    def insert(self, collection_name: str, data: dict) -> None:
        try:
            self.database[collection_name].insert(data)
        except Exception as error:
            print('ERROR: ', error)
            raise error

    def find(self, collection_name: str, query: Optional[Dict]) -> List[Dict]:
        try:
            results = self.database[collection_name].find(query)
        except Exception as error:
            print('ERROR: ', error)
            raise error
        return results

    def find_one(self, collection_name: str, query: Optional[Dict]) -> Dict:
        try:
            results = self.database[collection_name].find_one(query)
        except Exception as error:
            print('ERROR: ', error)
            raise error
        return results

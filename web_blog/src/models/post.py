from web_blog.src.common.database import Database
from typing import Optional, Dict, List
import uuid
import datetime


class BlogPost(object):

    def __init__(self, title: str, content: str, author: str, blog_id: str, _id: Optional[str] = None,
                 date: Optional[datetime.datetime] = None) -> None:
        self.title = title
        self.content = content
        self.author = author
        self.blog_id = blog_id

        self._id = _id if _id is not None else uuid.uuid4().hex
        self.date = date if date is not None else datetime.datetime.utcnow()
        pass

    def post_to_db(self, uri: str, db_name: str, collection_name: str) -> None:
        db = Database(uri=uri, db_name=db_name)
        db.insert(collection_name=collection_name, data=self.__dict__)

    @staticmethod
    def find_posts(uri: str, db_name: str, collection_name: str, query: Dict) -> List['BlogPost']:
        db = Database(uri=uri, db_name=db_name)
        results = db.find(collection_name=collection_name, query=query)
        results = [BlogPost.wrap_result(result) for result in results] if results else results
        return results

    @staticmethod
    def find_post(uri: str, db_name: str, collection_name: str, query: Dict) -> 'BlogPost':
        db = Database(uri=uri, db_name=db_name)
        result = db.find_one(collection_name=collection_name, query=query)
        result = BlogPost.wrap_result(result) if result else result
        return result

    @classmethod
    def wrap_result(cls, result):
        return cls(**result)

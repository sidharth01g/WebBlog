from web_blog.src.common.database import Database
from web_blog.configurations.blog_config import BlogConfig
from typing import Optional
import hashlib
from flask import session


class User(object):

    def __init__(self, email: str, password: str, _id: Optional[str] = None) -> None:
        self.email = email
        self.password = password
        self._id = _id if _id is not None else hashlib.sha1(self.email.encode()).hexdigest()

    @classmethod
    def wrap_result(cls, result):
        return cls(**result)

    @staticmethod
    def get_by_email(blog_config: BlogConfig, email: str) -> 'User':
        db = Database(uri=blog_config.uri, db_name=blog_config.db_name)
        result = db.find_one(collection_name=blog_config.collection_name_users, query={'email': email})
        result = User.wrap_result(result) if result else result
        return result

    @staticmethod
    def get_by_id(blog_config: BlogConfig, _id: str) -> 'User':
        db = Database(uri=blog_config.uri, db_name=blog_config.db_name)
        result = db.find_one(collection_name=blog_config.collection_name_users, query={'_id': _id})
        result = User.wrap_result(result) if result else result
        return result

    @classmethod
    def login_valid(cls, blog_config: BlogConfig, email: str, password: str) -> bool:
        result = cls.get_by_email(blog_config=blog_config, email=email)

        if result:  # User found in DB
            return result.password == password
        return False

    @classmethod
    def register(cls, blog_config: BlogConfig, email: str, password: str) -> bool:
        result = cls.get_by_email(blog_config=blog_config, email=email)
        if result:  # User already exists
            return False

        # User does not exist
        db = Database(uri=blog_config.uri, db_name=blog_config.db_name)
        user = User(email=email, password=password)
        db.insert(collection_name=blog_config.collection_name_users, data=user.__dict__)

        session['email'] = email
        return True

    @staticmethod
    def login(email: str):
        # login_valid has already been called
        session['email'] = email

    @staticmethod
    def logout():
        session['email'] = None

    # def save_to_db(self, blog_config: BlogConfig):
    #     db = Database(uri=blog_config.uri, db_name=blog_config.db_name)
    #     db.insert(collection_name=blog_config.collection_name_users, data=self.__dict__)

from web_blog.src.common.database import Database
from web_blog.configurations.blog_config import BlogConfig
from web_blog.src.models.blog import Blog
from typing import Optional, List
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
    def login(email: str) -> None:
        # login_valid has already been called
        session['email'] = email

    @staticmethod
    def logout() -> None:
        session['email'] = None

    def get_blogs_by_self(self, blog_config: BlogConfig) -> List[Blog]:
        query = {'author_id': self._id}
        results = Blog.find_blogs(blog_config=blog_config, query=query)
        return results

    def create_blog(self, blog_config: BlogConfig, title: str) -> None:
        blog = Blog(title=title, author=self.email, author_id=self._id)
        blog.create_blog(blog_config=blog_config)

    @staticmethod
    def create_post(blog_config: BlogConfig, post_title: str, post_content: str, blog_id: str) -> bool:
        blog = Blog.find_blog(blog_config=blog_config, query={'blog_id': blog_id})
        if not blog:
            # No such blog ID
            return False
        blog.create_post(blog_config=blog_config, post_title=post_title, post_content=post_content)
        return True

    @staticmethod
    def validate_email(email: str) -> bool:
        if '@' not in email or '.' not in email:
            return False
        if len(email.split('@')[0]) < 1 or len(email.split('@')[-1]) < 1:
            return False
        return True

    @staticmethod
    def validate_password(password: str) -> bool:
        if len(password) < 3:
            return False
        return True

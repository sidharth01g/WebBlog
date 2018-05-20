class BlogConfig(object):

    def __init__(self, uri: str, db_name: str, collection_name_posts: str, collection_name_users: str,
                 collection_name_blogs: str) -> None:
        self.uri = uri
        self.db_name = db_name
        self.collection_name_posts = collection_name_posts
        self.collection_name_users = collection_name_users
        self.collection_name_blogs = collection_name_blogs

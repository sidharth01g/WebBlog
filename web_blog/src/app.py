from flask import Flask, render_template, request, session
from web_blog.src.models.user import User
from web_blog.src.models.blog import Blog
from web_blog.configurations.blog_config import BlogConfig
from web_blog.logging.logger_base import Logging
from typing import Optional
import logging

logger = Logging.create_rotating_log(module_name=__name__, logging_directory='/tmp')
logger.info('Starting Blog Application')

uri = 'mongodb://127.0.0.1:27017'
db_name = 'blog_db'
collection_name_posts = 'blog_posts'
collection_name_users = 'blog_authors'
collection_name_blogs = 'blog_blogs'
blog_config = BlogConfig(uri=uri, db_name=db_name, collection_name_posts=collection_name_posts,
                         collection_name_blogs=collection_name_blogs, collection_name_users=collection_name_users)

app = Flask(__name__)

app.secret_key = "ajnefiun3iufnaieufn389hr9823hr"


# Initial setup
@app.before_first_request
def setup():
    pass


# API endpoints
@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(blog_config=blog_config, email=email, password=password):
        User.login(email=email)  # Add email to session

        return render_template("profile.html", email=session['email'])

    else:
        return render_template("message.html", message="Invalid user credentials")


@app.route('/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']

    if User.validate_email(email) is not True or User.validate_password(password) is not True:
        return render_template('message.html', message='Invalid email ID or password too weak')
        return False

    success = User.register(blog_config=blog_config, email=email, password=password)

    if success is True:
        return render_template("message.html", message="Registered {}".format(session['email']))
    else:
        session['email'] = None
        return render_template("message.html", message="Email ID {} is already registered".format(email))


@app.route('/blogs/<string:user_id>', methods=['GET'])
@app.route('/blogs')
def user_blogs(user_id: Optional[str] = None):
    # If no user ID is available get user ID from the email address of the session
    if user_id is None:
        if session['email'] is not None:
            user = User.get_by_email(blog_config=blog_config, email=session['email'])
            user_id = user._id
        else:
            render_template('message.html', message='No user')

    logger.info('user_id: {}'.format(user_id))
    # exit()

    user = User.get_by_id(blog_config=blog_config, _id=user_id)

    if not user:
        return render_template('message.html', message='User ID {} not found'.format(user_id))

    blogs = user.get_blogs_by_self(blog_config=blog_config)
    if not blogs:
        return render_template('message.html', message='User {} has no blogs yet'.format(user.email))

    return render_template('user_blogs.html', blogs=blogs, user=user)


@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id: Optional[str] = None):
    if blog_id is None:
        return render_template('message.html', message='No blog ID received')

    blog = Blog.find_blog(blog_config=blog_config, query={'_id': blog_id})
    if not blog:
        return render_template('message.html', message='No blogs found matching blog ID: {}'.format(blog_id))

    posts = blog.get_posts(blog_config=blog_config)
    if not posts:
        return render_template('message.html', message='No posts found matching blog {}'.format(blog.title))

    return render_template('blog_posts.html', blog=blog, posts=posts)


if __name__ == '__main__':
    app.run(port=4775)

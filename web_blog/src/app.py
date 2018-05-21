from flask import Flask, render_template, request, session
from web_blog.src.models.user import User
from web_blog.configurations.blog_config import BlogConfig

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
        return render_template("denied.html")


@app.route('/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']

    success = User.register(blog_config=blog_config, email=email, password=password)

    if success is True:
        return render_template("message.html", message="Registered {}".format(email))
    else:
        return render_template("message.html", message="Email ID {} is already registered".format(email))


if __name__ == '__main__':
    app.run(port=4775)

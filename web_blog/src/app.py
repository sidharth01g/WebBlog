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
def user_blogs(user_id: str):
    user_id = str(user_id)

    user = User.get_by_id(blog_config=blog_config, _id=user_id)
    if not user:
        return render_template('message.html', message='User ID {} not found'.format(user_id))

    blogs = user.get_blogs_by_self(blog_config=blog_config)
    if not blogs:
        return render_template('message.html', message='User ID {} has no blogs yet'.format(user_id))

    return render_template('user_blogs.html', blogs=blogs, user=user)


if __name__ == '__main__':
    app.run(port=4775)

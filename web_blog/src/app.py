from flask import Flask

app = Flask(__name__)


# API endpoints
@app.route('/')
def index():
    return("Hello world")


if __name__ == '__main__':
    app.run(port=4775)
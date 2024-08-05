from flask import Flask

app = Flask(__name__)


@app.route('/')
def goodbye_world():
    return 'Farewell, World! uuffff, ah wait a moment...'


if __name__ == '__main__':
    app.run()

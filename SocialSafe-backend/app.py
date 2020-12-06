from flask import Flask, jsonify, g
from flask_cors import CORS, cross_origin
from blueprints.restaurants import restaurant
from blueprints.users import user
from blueprints.reviews import review
from blueprints.favorites import favorite
import models
from flask_login import LoginManager

DEBUG = True
PORT = 8000

app = Flask(__name__)


app.secret_key = "This is a secret key. Here it is."

login_manager = LoginManager()

login_manager.init_app(app)


CORS(restaurant, origins=['http://localhost:3000', 'http://localhost:3000/add_restaurant'], supports_credentials=True)
CORS(user, origins=['http://localhost:3000'], supports_credentials=True)
CORS(review, origins=['http://localhost:3000'], supports_credentials=True)
CORS(favorite, origins=['http://localhost:3000'], supports_credentials=True)


app.register_blueprint(restaurant, url_prefix='/api/v1/restaurants')
app.register_blueprint(user, url_prefix='/api/v1/users')
app.register_blueprint(review, url_prefix='/api/v1/reviews')
app.register_blueprint(favorite, url_prefix='/api/v1/favorites')


@login_manager.user_loader
def load_user(user_id):
    try:
        print("loading the following user")
        user = models.User.get_by_id(user_id)

        return user

    except models.DoesNotExist:
        print("no current_user")
        return None


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


@app.route('/')
def idex():
    return "Hello"

@app.route('/sayhi/<username>')
def hello(username):
    return "Hello {}".format(username)
#
# if 'ON_HEROKU' in os.environ:
#   print('\non heroku!')
#   models.initialize()

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)

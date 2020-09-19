from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS, cross_origin
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager, UserMixin, login_user
import bcrypt
from flask_bcrypt import Bcrypt
import os


app = Flask(__name__) 

bcrypt = Bcrypt(app)

CORS(app)

basedir = os.path.abspath(__file__)

DATABASE_URL = os.environ.get('DATABASE_URL')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = ''
app.secret_key = b'\xd5\xe5\xdc\xa2\xef\xa0\xf2m\xf3 u\xf8""\xfc\x1a'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

migrate = Migrate(app, db, compare_type=True)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Joke(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False)
    content = db.Column(db.String(500), unique=False)

    def __init__(self, title, content):
        self.title = title
        self.content = content


class JokeSchema(ma.Schema):
    class Meta:
        fields = ('id','title', 'content')


joke_schema = JokeSchema()
jokes_schema = JokeSchema(many=True)


# Endpoint to create a new joke
@app.route('/joke', methods=["POST"])
def add_joke():
    title = request.json['title']
    content = request.json['content']

    new_joke = Joke(title, content)

    db.session.add(new_joke)
    db.session.commit()

    joke = Joke.query.get(new_joke.id)

    return joke_schema.jsonify(joke)


# Endpoint to query all jokes
@app.route("/jokes", methods=["GET"])
def get_jokes():
    all_jokes = Joke.query.all()
    result = jokes_schema.dump(all_jokes)
    return jsonify(result)


# Endpoint for querying a single joke
@app.route("/joke/<id>", methods=["GET"])
def get_joke(id):
    joke = Joke.query.get(id)
    return joke_schema.jsonify(joke)


# Endpoint for updating a joke
@app.route("/joke/<id>", methods=["PUT"])
def joke_update(id):
    joke = Joke.query.get(id)
    title = request.json['title']
    content = request.json['content']

    joke.title = title
    joke.content = content

    db.session.commit()
    return joke_schema.jsonify(joke)


# Endpoint for deleting a record
@app.route("/joke/<id>", methods=["DELETE"])
def joke_delete(id):
    joke = Joke.query.get(id)
    db.session.delete(joke)
    db.session.commit()

    # return joke_schema.jsonify(joke)
    return "Joke was successfully deleted"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.Text)


    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','name', 'email', 'password')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


# Endpoint to create a new user
@app.route('/user', methods=["POST"])
def add_user():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']

    new_user = User(name, email, password)

    db.session.add(new_user)
    db.session.commit()

    user = User.query.get(new_user.id)

    return user_schema.jsonify(user)

#endpoint to register user
@app.route('/register', methods=["POST", "GET"])
@cross_origin(supports_credentials=True)
def register():
    name = request.json.get('name')
    email = request.json.get('email')
    passwordToHash = request.json.get('passwordToHash')
    # name = request.json.get('name', None)
    # email = request.json.get('email', None)
    # passwordToHash = request.json.get('passwordToHash', None)

    if not name:
        return "Missing Name!!", 400
    if not email:
        return "Missing Email!", 400
    if not passwordToHash:
        return "Missing Password!", 400

    hashed = bcrypt.generate_password_hash(passwordToHash).decode('utf-8')

    new_user = User(name=name, email=email, password=hashed)
    db.session.add(new_user)
    db.session.commit()

    user = User.query.get(new_user.id)

    return f"Welcome {email}"


#endpoint to login user
@app.route('/login', methods=["POST", "GET"])
@cross_origin(supports_credentials=True)
def login():
    email = request.json.get('email')
    passwordToHash = request.json.get('passwordToHash')

    if not email:
        return "Missing Email!", 400
    if not passwordToHash:
        return "Missing Password!", 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return "User Not Found!", 404

    if bcrypt.check_password_hash(candidate, passwordToHash):
        login_user(user) #creates cookie/ session/ tells app user is logged in
        return f"Welcome Back {user.name}"
    else:
        return "Wrong Password!", 404


# Endpoint to query all users
@app.route("/users", methods=["GET"])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)


# Endpoint for querying a single user
@app.route("/user/<id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)


# Endpoint for updating a user
@app.route("/user/<id>", methods=["PUT"])
def user_update(id):
    user = User.query.get(id)
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']

    user.name = name
    user.email = email
    user.password = password

    db.session.commit()
    return user_schema.jsonify(user)


# Endpoint for deleting a record
@app.route("/user/<id>", methods=["DELETE"])
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    # return user_schema.jsonify(user)
    return "User was successfully deleted"



if __name__ == '__main__' :
    
    app.run(debug=True)
    manager.run()

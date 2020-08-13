from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os 

app = Flask(__name__)

# @app.route('/')
# def hello():
#     return "Hey Flask"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Joke(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False)
    content = db.Column(db.String(144), unique=False)

    def __init__(self, title, content):
        self.title = title
        self.content = content


class JokeSchema(ma.Schema):
    class Meta:
        fields = ('title', 'content')


joke_schema = JokeSchema()
jokes_schema = JokeSchema(many=True)


# Endpoint to create a new joke
@app.route('/joke', methods=["POST"])
def add_joke():
    # id = request.json['_id']
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
    # id = request.json['_id']
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



if __name__ == '__main__' :
    app.run(debug=True)
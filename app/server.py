from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.exc import IntegrityError
from socket import gethostname
from seed_data import generate_entry
import logging
import os
import pytest

app = Flask(__name__)
app.config['DEBUG'] = False
basedir = os.path.abspath(os.path.dirname(__file__))
sqlite_default = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')

DB_URI  = os.getenv('DB_URI', sqlite_default)
#print(DB_URI)
DB_SEED = os.getenv('DB_SEED', False)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
print(app.config['SQLALCHEMY_DATABASE_URI'])
db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

def generate_hello_message():
    hostname = gethostname()
    message = f"hello from {hostname}"
    return message

def seed_database(records):
    print(type(DB_SEED))
    if bool(DB_SEED) == True:
        print("its true")
        objects = []
        for each in range(0,records):
            person_details = generate_entry()
            username = '{fname}.{lname}'.format(fname=person_details['first_name'], lname=person_details['last_name'])
            objects.append(User(username, person_details['email_address']))
        db.session.bulk_save_objects(objects)
        db.session.commit()
        del objects
    return True

@app.before_first_request
def setup_logging():
    db.create_all()
    seed_database(5)
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)
    
@app.route('/hostname')
def home():
    message = generate_hello_message()
    return message

@app.route('/api/users', methods=["POST"])
def add_user():
    username = request.json['username']
    email = request.json['email']
    try:
        new_user = User(username, email)
        db.session.add(new_user)
        db.session.commit()
        result = user_schema.dump(new_user)
    except IntegrityError:
        db.session.rollback()
        result = {"message": "user {} already exists".format(username)}
    return jsonify(result)

@app.route('/api/users', methods=['GET'])
def get_user():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

@app.route('/api/users/<id>', methods=['GET'])
def user_detail(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

@app.route('/api/users/<id>', methods=['PUT'])
def user_update(id):
    user = User.query.get(id)
    username = request.json['username']
    email = request.json['email']
    user.email = email
    user.username = username
    db.session.commit()
    return user_schema.jsonify(user)

@app.route('/api/users/<id>', methods=['DELETE'])
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)

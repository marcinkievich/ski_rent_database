from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:karolina13@localhost/postgres'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Skis(db.Model):
    __tablename__ = 'skis'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    length = db.Column(db.Integer)
    softness = db.Column(db.Integer)
    price = db.Column(db.Integer)
    availability = db.Column(db.Boolean)

    def __init__(self, name, length, softness, price, availability):
        self.name = name
        self.length = length
        self.softness = softness
        self.price = price
        self.availability = availability

def insert_loop():
    mark = ['head', 'fischer', 'rossignol', 'atomic', 'salomon']
    send_data = []
    for j in range(5):
        softness = (j +1 ) * 2
        for i in range(10):
            id = (i + 1) * (j + 1)
            length = 100 + 2 * i * j
            price = 50 + j;
            availability = 'True';
            temp = [id, mark, length, softness, price, availability]
            send_data.append(temp)




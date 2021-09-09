from flask import Flask, render_template
from flask_restful import Api
from flask_jwt import JWT
from db import db

from security import authenticate, identity
from resources.user import UserRegister
from resources.visitor import Visitor, VisitorList
from resources.visitor_group import VisitorGroup, VisitorGroupList


app = Flask(__name__)
#  Tell SQL Alchemy where the db is
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# Turn off the flask sql alchemy tracker and use the more efficieny sql_alchemy tracker
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'my_first_flask_app_key'
api = Api(app)

# Ask SQL Alchemy to create database and tables
# Has to run before first request
@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)

visitors = []


# Index is long form scrolling splash page
@app.route('/')
def index():
    return render_template('index.html')


# Contact page is just a form
@app.route('/contact')
def contact():
    return render_template('contact.html')
        

api.add_resource(Visitor, '/visitor/<string:name>')
api.add_resource(VisitorList, '/visitors')
api.add_resource(VisitorGroup, '/visitor_group/<string:name>')
api.add_resource(VisitorGroupList, '/visitor_groups')
api.add_resource(UserRegister, '/register')


if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True)
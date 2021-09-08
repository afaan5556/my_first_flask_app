from flask import Flask, render_template
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from visitor import Visitor, VisitorList


app = Flask(__name__)
app.secret_key = 'my_first_flask_app_key'
api = Api(app)

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
        

api.add_resource(VisitorList, '/visitors')
api.add_resource(Visitor, '/visitor/<string:name>')
api.add_resource(UserRegister, '/register')


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from user import UserRegister

users = [
{
    'name': 'afaan.naqvi',
}]


app = Flask(__name__)
app.secret_key = 'my_first_flask_app_key'
api = Api(app)

jwt = JWT(app, authenticate, identity)

users = []


# Index is long form scrolling splash page
@app.route('/')
def index():
    return render_template('index.html')


# Contact page is just a form
@app.route('/contact')
def contact():
    return render_template('contact.html')


# CRUD functionality for users
class User(Resource):
    parser = reqparse.RequestParser()
    for i in ['name', 'first_name', 'last_name', 'email', 'phone']:
        parser.add_argument(i,
            type=str,
            required=True,
            help="This field ca be left blank"
            )

    @jwt_required()
    def get(self, name):
        # Filter function gives a filter object. Turn into list and get next item in list
        user = next(filter(lambda x: x['name'] == name, users), None)
        return {'user': user}, 200 if user else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, users), None) is not None:
            return {'message': "A user with name '{}' already exists.".format(name)}, 400

        data = User.parser.parse_args()

        user = {
        'name': data['name'],
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'email': data['email'],
        'phone': data['phone']
        }
        users.append(user)
        return user, 201

    def delete(self, name):
        global users
        users = list(filter(lambda x: x['name'] != name, users))
        return {'message:': 'Item with name {} deleted'.format(name)}

    def put(self, name):
        data = User.parser.parse_args()

        user = next(filter(lambda x: x['name'] == name, users), None)
        if user is None:
            user = {
            'name': data['name'],
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'phone': data['phone']
            }
            users.append(user)
        else:
            user.update(data)
        return user


class UserList(Resource):
    def get(self):
        return {'users': users}
        

api.add_resource(UserList, '/users')
api.add_resource(User, '/user/<string:name>')
api.add_resource(UserRegister, '/register')

# Get all users
@app.route('/users')
def crud():
    return jsonify({'users': users})


# Create a user
@app.route('/user', methods=['POST'])
def post_user():
    request_data = request.get_json()
    new_user = {
    'name': request_data['name'],
    'first_name': request_data['first_name'],
    'last_name': request_data['last_name'],
    'email': request_data['email'],
    'phone': request_data['phone'],
    'hobbies': [],
    }
    users.append(new_user)
    return jsonify(new_user)

# Get a user
@app.route('/user/<string:name>')
def get_user(name):
    for user in users:
        if user['name'] == name:
            return jsonify(user)
    return jsonify({'message': 'user not found'})



if __name__ == "__main__":
    app.run(debug=True)
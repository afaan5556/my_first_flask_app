from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy

users = [
{
    'name': 'afaan.naqvi',
    'first_name': 'Afaan',
    'last_name': 'Naqvi',
    'email': 'afaan.naqvi@gmail.com',
    'phone': '+491709312851',
    'hobbies': [
    {
    'name': 'football',
    'level': 'love'
    },
    {
    'name': 'music',
    'level': 'enjoy'
    }]
}]


app = Flask(__name__)
app.secret_key = "Secret Key"

#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Index is long form scrolling splash page
@app.route('/')
def index():
    return render_template('index.html')


# Contact page is just a form
@app.route('/contact')
def contact():
    return render_template('contact.html')


# CRUD Functionality starts here - Users and Hobbies
@app.route('/crud/user')
def crud():
    return jsonify({'users': users})


# Create a user
@app.route('/crud/user', methods=['POST'])
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
@app.route('/crud/user/<string:name>')
def get_user(name):
    for user in users:
        if user['name'] == name:
            return jsonify(user)
    return jsonify({'message': 'user not found'})


# Get all users
@app.route('/crud/user')
def get_users():
    return jsonify({'users': users})


# Create a user hobby
@app.route('/crud/user/<string:name>/hobby', methods=['POST'])
def post_user_hobby(name):
    request_data = request.get_json()
    for user in users:
        if user['name'] == name:
            new_hobby = {
            'name': request_data['name'],
            'level': request_data['level']
            }
            user['hobbies'].append(new_hobby)
            return jsonify(new_hobby)
    return jsonify({'message': 'user not found'})


# Get user hobbies
@app.route('/crud/user/<string:name>/hobby')
def get_user_hobbies(name):
    for user in users:
        if user['name'] == name:
            return jsonify(user['hobbies'])
    return 'User not found'
    


if __name__ == "__main__":
    app.run(debug=True)
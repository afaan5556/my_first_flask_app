from flask import Flask, render_template, make_response, request, jsonify, redirect
from models.visitor import VisitorModel
# from flask_restful import Api
from flask_jwt import JWT
from db import db
from security import authenticate, identity


app = Flask(__name__)
#  Tell SQL Alchemy where the db is
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# Turn off the flask sql alchemy tracker and use the more efficieny sql_alchemy tracker
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'my_first_flask_app_key'
# api = Api(app)

# Ask SQL Alchemy to create database and tables
# Has to run before first request
@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)


# Index is long form scrolling splash page
@app.route('/')
def index():
    return render_template('index.html')


# Contact page is just a form
@app.route('/contact')
def contact():
    return render_template('contact.html')


# Visitors table view
@app.route('/visitors')
def visitors():
    headers = {'Content-Type': 'text/html'}
    visitors = [visitor.json() for visitor in VisitorModel.query.all()]
    return make_response(render_template('visitors.html', visitors=visitors), 200, headers)

# Visitor CRUD routes
@app.route('/visitor', methods=['POST', 'PUT', 'DELETE'])
def visitor():
    if request.method == 'POST':
        data = {'name': request.form['name'],
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'phone': request.form['phone']
        }

        visitor = VisitorModel(data['name'], data['first_name'], data['last_name'], data['email'], data['phone'])

        try:
            visitor.save_to_db()
        except:
            {'message': 'An error occurred inserting the visitor'}, 500

        return redirect("/visitors", code=302)
    elif request.method == 'PUT':
        pass

    else:
        pass



if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True)
from flask import Flask, render_template, make_response, request, jsonify, redirect, flash, url_for
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
@app.route('/visitor/add', methods=['POST'])
def add():
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
        {'message': 'An error occurred adding the visitor'}, 500

    return redirect(url_for('visitors'), code=302)


@app.route('/visitor/<name>/delete', methods=('GET', 'POST'))
def delete(name):
    visitor = VisitorModel.find_by_name(name)

    if not visitor:
        flash('Visitor with name {} was not found!'.format(name))
        return redirect(url_for('visitors'), code=404)
    else:
        try:
            visitor.delete_from_db()
        except:
            flash('Problem deleting visitor with name {}!'.format(name))
            return redirect("/visitors", code=500)

    flash('Visitor {} was successfully deleted!'.format(name))
    return redirect(url_for('visitors'))



if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True)
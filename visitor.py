import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Visitor(Resource):
    parser = reqparse.RequestParser()
    for i in ['name', 'first_name', 'last_name', 'email', 'phone']:
        parser.add_argument(i,
            type=str,
            required=True,
            help="This field cannot be left blank"
            )

    @jwt_required()
    def get(self, name):
        try:
            visitor = self.find_visitor_by_name(name)
        except:
            {'message': 'An error occurred inserting the visitor'}, 500

        if visitor:
            return visitor
        return {'message': 'Visitor with name {} not found'.format(name)}, 404

    @classmethod
    def find_visitor_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM visitors WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'visitor': {'name': row[0], 'first_name': row[1], 'last_name': row[2], 'email': row[3], 'phone': row[4]}}


    @classmethod
    def insert_visitor(cls, visitor):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO visitors VALUES (NULL, ?, ?, ?, ?, ?)"
        result = cursor.execute(query, (visitor['name'], visitor['first_name'], visitor['last_name'], visitor['email'], visitor['phone']))
        
        connection.commit()
        connection.close()


    @classmethod
    def update_visitor(cls, visitor):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE visitors SET first_name=?, last_name=?, email=?, phone=? WHERE name=?"
        result = cursor.execute(query, (visitor['first_name'], visitor['last_name'], visitor['email'], visitor['phone'], visitor['name']))
        
        connection.commit()
        connection.close()


    def post(self, name):
        if Visitor.find_visitor_by_name(name):
            return {'message': "A user with name '{}' already exists.".format(name)}, 400


        data = Visitor.parser.parse_args()

        visitor = {
        'name': data['name'],
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'email': data['email'],
        'phone': data['phone']
        }
        try:
            Visitor.insert_visitor(visitor)
        except:
            {'message': 'An error occurred inserting the visitor'}, 500

        return visitor, 201

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM visitors WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Visitor with name {} deleted'.format(name)}


    def put(self, name):
        data = Visitor.parser.parse_args()

        try:
            visitor = Visitor.find_visitor_by_name(name)
        except:
            {'message': 'An error occurred inserting the visitor'}, 500

        updated_visitor = {
        'name': data['name'],
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'email': data['email'],
        'phone': data['phone']
        }

        if visitor is None:
            try:
                Visitor.insert_visitor(updated_visitor)
            except:
                {'message': 'An error occurred inserting the visitor'}, 500
        else:
            try:
                Visitor.update_visitor(updated_visitor)
            except:
                {'message': 'An error occurred updating the visitor'}, 500   

        return updated_visitor


class VisitorList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM visitors"
        result = cursor.execute(query)
        result = result.fetchall()

        connection.close()

        visitors = [{'id': row[0], 'name': row[1], 'first_name': row[2], 'last_name': row[3], 'email': row[4], 'phone': row[5]} for row in result]


        return {'visitors': visitors}
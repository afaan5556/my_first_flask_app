from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.visitor import VisitorModel


class Visitor(Resource):
    parser = reqparse.RequestParser()
    for i in ['name', 'first_name', 'last_name', 'email', 'phone', 'visitor_group_id']:
        parser.add_argument(i,
            type=str,
            required=True,
            help="This field cannot be left blank"
            )

    @jwt_required()
    def get(self, name):
        try:
            visitor = VisitorModel.find_by_name(name)
        except:
            {'message': 'An error occurred finding the visitor with name {}'.format(name)}, 500

        if visitor:
            return visitor.json()
        return {'message': 'Visitor with name {} not found'.format(name)}, 404

    def post(self, name):
        if VisitorModel.find_by_name(name):
            return {'message': "A user with name '{}' already exists.".format(name)}, 400

        data = Visitor.parser.parse_args()

        visitor = VisitorModel(name, data['first_name'], data['last_name'], data['email'], data['phone'], data['visitor_group_id'])
        
        try:
            visitor.save_to_db()
        except:
            {'message': 'An error occurred inserting the visitor'}, 500

        return visitor.json(), 201

    def delete(self, name):
        visitor = VisitorModel.find_by_name(name)
        if visitor:
            visitor.delete_from_db()

        return {'message': 'Visitor with name {} deleted'.format(name)}


    def put(self, name):
        data = Visitor.parser.parse_args()

        try:
            visitor = VisitorModel.find_by_name(name)
        except:
            {'message': 'An error occurred inserting the visitor'}, 500

        if visitor is None:
            visitor = VisitorModel(name, data['first_name'], data['last_name'], data['email'], data['phone'], data['visitor_group_id'])
        else:
            visitor.first_name = data['first_name']
            visitor.last_name = data['last_name']
            visitor.email = data['email']
            visitor.phone = data['phone']
            visitor.visitor_group_id = data['visitor_group_id']

        visitor.save_to_db()

        return visitor.json()


class VisitorList(Resource):
    def get(self):
        return {'visitors': [item.json() for item in VisitorModel.query.all()]}

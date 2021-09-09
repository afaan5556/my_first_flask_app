from flask_restful import Resource
from models.visitor_group import VisitorGroupModel

class VisitorGroup(Resource):
	def get(self, name):
		visitor_group = VisitorGroupModel.find_by_name(name)
		if visitor_group:
			return visitor_group.json()
		return {'message': 'Visitor Group {} not found'.format(name)}, 404

	def post(self, name):
		if VisitorGroupModel.find_by_name(name):
			return {'message': 'A Visitor Group with the name {} already exists'.format(name)}, 400

		visitor_group = VisitorGroupModel(name)
		try:
			visitor_group.save_to_db()
		except:
			return {'message': 'An error occured while creating the visitor group'}, 500
		
		return {'message': 'Visitor group {} created successfully'.format(name)}, 200

	def delete(self, name):
		visitor_group = VisitorGroupModel.find_by_name(name)
		if visitor_group:
			visitor_group.delete_from_db()

		return {'message': 'Visitor Group {} deleted'.format(name)}


class VisitorGroupList(Resource):
	def get(self):
		return {'visitor_groups': [visitor_group.json() for visitor_group in VisitorGroupModel.query.all()]}
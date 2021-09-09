from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
	parser = reqparse.RequestParser()
	for i in ['username', 'password']:
		parser.add_argument(i,
			type=str,
			required=True,
			help='This field can not be blank.')

	def post(self):
		data = UserRegister.parser.parse_args()

		if UserModel.find_by_username(data['username']):
			return {"message": "A user with the username {} already exists".format(data['username'])}

		user = UserModel(**data) # Same as (data['username'], data['password']
		user.save_to_db()

		return {"message": "User {} created successfully.".format(data['username'])}, 201

from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token
import sqlite3
from models.user import UserModel

parser = reqparse.RequestParser()
parser.add_argument('username',
                    type=str,
                    required=True,
                    help="This field cannot be left blank!"
                    )
parser.add_argument('password',
                    type=str,
                    required=True,
                    help="This field cannot be left blank!"
                    )


class User(Resource):

    @classmethod
    def get(user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @classmethod
    def delete(user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User does not exist'}, 404
        user.delete()
        return {'message': 'User deleted'}, 200



class Register(Resource):

    def post(self):
        data = parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "User with that username already exists."}, 400

        user = UserModel(data["username"], data["password"])
        user.save()

        return {"message": "User created successfully."}, 201



class Login(Resource):
    

    def post(self):
        data = parser.parse_args()
        user = UserModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)

            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {'message': 'User does not exist'}
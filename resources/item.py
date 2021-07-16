from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt
import sqlite3

from models.item import ItemModel

class Item(Resource):
    TABLE_NAME = 'items'

    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Require a store ID!"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):

        data = Item.parser.parse_args()

        if ItemModel.find_by_name(data['name']):
            return {'message': "An item with name '{}' already exists.".format(data['name'])}

        item = ItemModel(data['name'], data['price'], data["store_id"])

        try:
            item.save()
        except:
            return {"message": "An error occurred inserting the item."}

        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        claims = get_jwt()
        if not claims['is_admin']:
            return {'message': 'You need to be an admin'}
        item = ItemModel.find_by_name(name)
        if item:
            item.delete()
            return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            try:
                item = ItemModel(data["name"], data["price"], data["store_id"])
            except:
                return {"message": "An error occurred inserting the item."}
        else:
            try:
                item["price"] = data["price"]
            except:
                return {"message": "An error occurred updating the item."}

        item.save()
        return item.json()


class ItemList(Resource):
    TABLE_NAME = 'items'

    def get(self):
        return {'items': [item.json() for item in ItemModel.get_all()]}
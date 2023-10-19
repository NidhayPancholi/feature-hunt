
from flask import request, jsonify, Response
from flask import json
from app import app
import pandas as pd
from bson.json_util import dumps
from bson.objectid import ObjectId
from db_init import product_records


class Product:
    def __init__(self) -> None:
        self.db=product_records
    
    def get_products(self):
        #get timestamp sorted products
        data = self.db.find().sort('timestamp', -1)
        product_data=[]
        for product in data:
            product['_id']=str(product['_id'])
            product_data.append(product)
            
        return product_data
        
    def get_product(self,product_id):
        data = self.db.find_one({'_id': ObjectId(product_id)})
        data['_id']=str(data['_id'])
        return data
    
    def add_product(self,product_input):
        x=self.db.insert_one(product_input)
        return {'ProductID': str(x.inserted_id), 'message': 'Product added successfully'}
    
    def delete_product(self,product_name):
        db_response = self.db.delete_one({'name': product_name})
        if db_response.deleted_count == 1:
            response = {'ok': True, 'message': 'record deleted'}
        else:
            response = {'ok': False, 'message': 'no record found'}
        return jsonify(response), 200
    
    def get_sorted_products(self,sort_by):
        data = self.db.find().sort(sort_by, -1)
        return data

        
    def add_view(self,product_id):
        db_response = self.db.update_one({'_id': ObjectId(product_id)},{'$inc': {'views': 1}})
        if db_response.modified_count == 1:
            response = {'ok': True, 'message': 'record updated'}
        else:
            response = {'ok': False, 'message': 'no record found'}
        return jsonify(response), 200

    def add_vote(self,product_id):
        db_response = self.db.update_one({'_id': ObjectId(product_id)},{'$inc': {'votes': 1}})
        if db_response.modified_count == 1:
            response = {'ok': True, 'message': 'record updated'}
        else:
            response = {'ok': False, 'message': 'no record found'}
        return jsonify(response), 200
    
    def remove_vote(self,product_id):
        db_response = self.db.update_one({'_id': ObjectId(product_id)},{'$inc': {'votes': -1}})
        if db_response.modified_count == 1:
            response = {'ok': True, 'message': 'record updated'}
        else:
            response = {'ok': False, 'message': 'no record found'}
        return jsonify(response), 200

    def add_feature(self,product_id,feature):
        db_response = self.db.update_one({'_id': ObjectId(product_id)},{'$push': {'features': feature}})
        if db_response.modified_count == 1:
            response = {'ok': True, 'message': 'record updated'}
        else:
            response = {'ok': False, 'message': 'no record found'}
        return jsonify(response), 200
    
    
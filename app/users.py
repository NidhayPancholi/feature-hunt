from flask import request, jsonify, Response
from flask import json
import pandas as pd
from bson.json_util import dumps
from bson.objectid import ObjectId
from db_init import records


class Users:
    def __init__(self):
        self.db=records
    
    def get_users(self):
        data = self.db.find()
        return data
    
    def get_user(self,user_id):
        data = self.db.find_one({'_id': ObjectId(user_id)})
        data['_id']=str(data['_id'])
        return data
    
    def get_user_by_email(self,email):
        data = self.db.find_one({'email': email})
        if data:
            data['_id']=str(data['_id'])
        return data
    
    def add_user(self,user_input):
        x=self.db.insert_one(user_input)
        print(x.inserted_id)
        return {'UserID': str(x.inserted_id), 'message': 'User added successfully'}, 200
    
    def delete_product(self,user_name):
        db_response = self.db.delete_one({'name': user_name})
        if db_response.deleted_count == 1:
            response = {'ok': True, 'message': 'record deleted'}
        else:
            response = {'ok': True, 'message': 'no record found'}
        return jsonify(response), 200
    
    
    def add_vote(self,user_id,post_id):
        #get user from database and add post_id to vote set
        db_response = self.db.update_one({'_id': ObjectId(user_id)},{'$addToSet': {'votes': post_id}})
        
        if db_response.modified_count == 1:
            response = {'ok': True, 'message': 'vote added'}
        else:
            response = {'ok': False, 'message': 'vote not added'}
        return jsonify(response), 200
    
    def remove_vote(self,product_id,post_id):
        #get user from database and remove post_id to vote set
        db_response = self.db.update_one({'_id': ObjectId(product_id)},{'$pull': {'votes': post_id}})
        if db_response.modified_count == 1:
            response = {'ok': True, 'message': 'vote removed'}
        else:
            response = {'ok': False, 'message': 'vote not removed'}
        return jsonify(response), 200
    
    def add_product(self,user_id,product_id):
        db_response = self.db.update_one({'_id': ObjectId(user_id)},{'$push': {'products': product_id}})
        
        if db_response.modified_count == 1:
            response = {'ok': True, 'message': 'product added'}
        else:
            response = {'ok': False, 'message': 'product not added'}
        return jsonify(response), 200
    
    def add_company(self,user_id,company_id):
        db_response = self.db.update_one({'_id': ObjectId(user_id)},{'$push': {'companies': company_id}})
        
        if db_response.modified_count == 1:
            response = {'ok': True, 'message': 'company added'}
        else:
            response = {'ok': False, 'message': 'company not added'}
        return jsonify(response), 200
    
    def get_user_companies(self,user_id):
        data = self.db.find_one({'_id': ObjectId(user_id)})
        data['_id']=str(data['_id'])
        return data['companies']
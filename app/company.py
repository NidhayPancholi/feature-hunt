
from flask import request, jsonify, Response,session
from flask import json
from bson.objectid import ObjectId
from db_init import company_records
from products import Product

class Company:
    def __init__(self) -> None:
        self.db=company_records
    
    def get_companies(self):
        data = self.db.find()
        return data
    
    def get_company(self,company_id):
        data = self.db.find_one({'_id': ObjectId(company_id)})
        return data
    
    def add_company(self,company_input):
        x=self.db.insert_one(company_input)
        return {'CompanyID': str(x.inserted_id), 'message': 'Product added successfully'}
    
    def delete_company(self,company_name):
        db_response = self.db.delete_one({'name': company_name})
        if db_response.deleted_count == 1:
            response = {'ok': True, 'message': 'record deleted'}
        else:
            response = {'ok': False, 'message': 'no record found'}
        return jsonify(response), 200
    
    def get_total_votes_for_company(self,company_id):
        company = self.db.find_one({'_id': ObjectId(company_id)})
        total_votes = 0
        for product_id in company['products']:
            product = Product.get_product(product_id)
            total_votes += product['votes']
        return company['votes']
    
    def add_product_to_company(self,company_id,product_id):
        company = self.db.find_one({'_id': ObjectId(company_id)})
        company['products'].append(product_id)
        self.db.save(company)
        return True
    
    

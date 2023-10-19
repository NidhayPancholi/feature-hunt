# pylint: disable=wrong-import-position,pointless-string-statement,undefined-variable,line-too-long

from flask import jsonify
from flask import request,render_template,session,redirect,url_for
from app import app
from products import Product
from users import Users
from company import Company

companydb=Company()
userdb=Users()
productdb = Product()

#################################################################################
##       Function: add_product
##       Description: This post request is used to gather all the information from
##                    the project form and send it to the database to be stored
##       Inputs:
##           - NA
##       Outputs:
##           - Returns true or false if new project is able to be added
#################################################################################
@app.route("/addproduct", methods=['POST','GET'])
def add_product():
    if 'userid' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        product_name = request.form.get("name")
        product_description = request.form.get("description")
        tags = request.form.get("tags").split(',')
        company_id=request.form.get("company")
        get_company=companydb.get_company(company_id)
        product_input = {'name': product_name, 'description': product_description,
                            'tags': tags, 'features': [],'votes':0,'views':0,'created_by':session['userid'],'features':[],'company_id':company_id,'company_name':get_company['name']}


        res=productdb.add_product(product_input)
        companydb.add_product_to_company(company_id,res['ProductID'])
        userdb.add_product(session['userid'],res['ProductID'])
        return redirect(url_for('product_feed'))
    else:
        user=userdb.get_user(session['userid'])
        user_companies=[]
        for company_id in user['companies']:
            user_companies.append([company_id,companydb.get_company(company_id)['name']])



        return render_template("productform.html",user_companies=user_companies)



@app.route("/getproducts", methods=['GET'])
def get_products():
    res=productdb.get_products()
    return res

@app.route("/getProduct/<product_id>", methods=['GET'])
def get_product(product_id):
    res=productdb.get_product(product_id)
    print(type(res))
    return res


@app.route("/deleteProduct/<product_name>", methods=['DELETE'])
def delete_product(product_name):
    res=productdb.delete_product(product_name)
    return res

@app.route("/getSortedProducts/<sort_by>", methods=['GET'])
def get_sorted_products(sort_by):
    res=productdb.get_sorted_products(sort_by)
    return res

@app.route("/addView/<product_id>", methods=['GET'])
def add_view(product_id):
    res=productdb.add_view(product_id)
    return res

@app.route("/addVote/<product_id>", methods=['GET'])
def add_vote(product_id):
    res=productdb.add_vote(product_id)
    return redirect(url_for('product_feed'))


@app.route("/removeVote/<product_id>", methods=['GET'])
def remove_vote(product_id):
    res=productdb.remove_vote(product_id)
    return redirect(url_for('product_feed'))


@app.route('/feed', methods=['GET'])
def product_feed():
    #if 'email' not in session:
     #   return redirect(url_for('login'))
    
    products=productdb.get_products()
    return render_template('productfeed.html',products=products)


#TODO: Fetch Product from backend
@app.route('/viewproduct/<product_id>', methods=['GET'])
def view_product(product_id):
    #if 'userid' not in session:
     #   return redirect(url_for('login'))
    productdb.add_view(product_id)
    product=productdb.get_product(product_id)
    return render_template('productpage.html',product=product)
    


@app.route("/suggestfeature/<product_id>", methods=['GET','POST'])
def suggest_feature(product_id):
    #if 'userid' not in session:
     #   return redirect(url_for('login'))
    if request.method == 'POST':
        feature_name = request.form.get("name")
        feature_description = request.form.get("description")
        feature_input = {'name': feature_name, 'description': feature_description,
                            'votes':0}
        res=productdb.add_feature(product_id,feature_input)
        return redirect(url_for('view_product',product_id=product_id))
    else:
        return render_template("featureform.html",product_id=product_id)
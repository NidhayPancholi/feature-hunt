# pylint: disable=wrong-import-position,pointless-string-statement,undefined-variable,line-too-long

from flask import jsonify
from flask import request,render_template,session,redirect,url_for
from app import app
from company import Company
from users import Users
from products import Product

productdb=Product()
userdb=Users()
companydb = Company()

#################################################################################
##       Function: add_product
##       Description: This post request is used to gather all the information from
##                    the project form and send it to the database to be stored
##       Inputs:
##           - NA
##       Outputs:
##           - Returns true or false if new project is able to be added
#################################################################################
@app.route("/addcompany", methods=['Post','GET'])
def add_company():
    if 'email' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        company_name = request.form.get("name")
        company_description = request.form.get("description")
        tags = request.form.get("tags").split(',')

        company_input = {'name': company_name, 'description': company_description,
                            'tags': tags,'views':0,'products':[],"created_by":session['userid']}


        res=companydb.add_company(company_input)
        userdb.add_company(session['userid'],res['CompanyID'])
        return redirect(url_for('product_feed'))
    else:
        return render_template("companyform.html")


@app.route("/getcompanies", methods=['GET'])
def get_companies():
    res=companydb.get_companies()
    return res


@app.route("/deletecompany/<company_name>", methods=['DELETE'])
def delete_company(company_name):
    res=companydb.delete_company(company_name)
    return res

@app.route('/company/<company_id>', methods=['GET'])
def view_company(company_id):
    data= companydb.get_company(company_id)
    product_list=[]
    for product in data['products']:
        product_list.append(productdb.get_product(product))
    print(product_list,data)
    return render_template('CompanyPage.html',data=data,product_list=product_list)
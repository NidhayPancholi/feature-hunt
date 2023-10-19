# pylint: disable=wrong-import-position,pointless-string-statement,undefined-variable,line-too-long
import json
from flask import request, session, redirect, url_for,render_template
from flask import Response
import bcrypt
from app import app
from users import Users

userdb=Users()

#################################################################################
##       Function: signup
##       Description: Post request to register a new user, will give error if user is already
##                    registered
##       Inputs:
##           - NA
##       Outputs:
##           - message: output if user is registered successful or not
#################################################################################
@app.route("/signup", methods=['POST',"GET"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    
    #implementation for POST
    user = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    email_found = userdb.get_user_by_email(email)
    print(email_found)
    

    if email_found:
        error_dict = {
            "code": 409,
            "message": "This email already is already registered.",
            "email": email
        }
        message = json.dumps(error_dict)
        return message

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user_input = {'name': user, 'email': email, 'password': hashed, 'votes': [],'products':[],'companies':[]}
    res,code=userdb.add_user(user_input)
    if code==200:
        session["email"] = email
        session["name"] = user
        session['userid']=res['UserID']

        return redirect(url_for('logged_in'))
    else:
        return '<p>Something went wrong!. <a href="http://localhost:5000/signup">Signup again</a></p>'

redirect_url = 'http://localhost:5000/'

#################################################################################
##       Function: logged_in
##       Description: Checks if there is a session
##       Inputs:
##           - NA
##       Outputs:
##           - Sends a valid message or redirects to login url
#################################################################################
@app.route('/logged_in', methods=["POST", "GET"])
def logged_in():
    if "email" in session:
        return redirect(url_for('product_feed'))
    else:
        return redirect(url_for('login'))

#################################################################################
##       Function: login
##       Description: Checks if user and email is in database to login
##       Inputs:
##           - NA
##       Outputs:
##           - Returns valid or invalid message if user can login
#################################################################################
@app.route("/login", methods=["POST", "GET"])
def login():
    if 'email' in session:
        return redirect(url_for('product_feed'))
    if request.method == "POST":
        email = request.form.get("email", None)
        password = request.form.get("password", None)

        if password is None or email is None:

            return Response(status=403)

        email_found = userdb.get_user_by_email(email)
        
        if email_found!="null":
            email_val = email_found['email']
            password_check = email_found['password']
            name = email_found['name']

            if bcrypt.checkpw(password.encode('utf-8'), password_check):
                session["email"] = email_val
                session["name"] = name
                session['userid']=email_found['_id']
                print("Logged in successfully!")
                return redirect(url_for('product_feed'))
            else:
                #return html that the password was incorrect and a redirect link to the login page
                return '<p>Invalid Password!. <a href="http://localhost:5000/login">Login again</a></p>'
        else:
            #return html that the password was incorrect and a redirect link to the login page
            return '<p>Invalid Email!. <a href="http://localhost:5000/login">Login again</a></p>'
            
    else:
        return render_template("login.html")
    

#################################################################################
##       Function: logout
##       Description: Checks if user is in session and removes them from it
##       Inputs:
##           - NA
##       Outputs:
##           - Successful or Unsuccessful Message
#################################################################################
@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        
        #delete the entire session
        session.clear()
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
import os
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

result = ""

app = Flask(__name__)
app.secret_key = "mysecretkey"
app.config["MONGO_DBNAME"] = 'cook_book'
app.config["MONGO_URI"] = 'mongodb+srv://jraysim:OrganD0NER@myfirstcluster-hdrnx.mongodb.net/cook_book?retryWrites=true&w=majority'

mongo = PyMongo(app)


@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html", user="")
    
@app.route('/sign_up')
def sign_up():
    return render_template('signup.html', error = "")
    
@app.route('/add_user/success')
def add_user_success():
    return render_template('signupsuccess.html')

@app.route('/add_user/failed', methods=["POST", "GET"])
def add_user():
    newuser = mongo.db.users.count({'username': request.form.get('username')})
    if request.method == 'POST':
        if newuser > 0:
            error = "{0} has already been taken".format(request.form.get('username'))
        else:
            flash("Your account has been created, log in to continue")
            return render_template('signin.html')
    return render_template('signup.html', error=error)
        
@app.route('/sign_in')
def sign_in():
    return render_template('signin.html', error = "")
    
@app.route('/home/logged_in', methods=["POST"])
def log_in():
    users = mongo.db.users.find({'username': request.form.get('username'), 'password': request.form.get('password')})
    if request.method == 'POST':
        if users.count() > 0:
            user = mongo.db.users.find_one({'username': request.form.get('username'), 'password': request.form.get('password')})
            return render_template('home.html', user=user)
        else:
            error = "Sorry, your Username or Password is incorrect"
            return render_template('signin.html', error = error)
            
@app.route('/home/<username>')
def user_home(username):
    user = mongo.db.users.find_one({'username': username})
    return render_template('home.html', user=user)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
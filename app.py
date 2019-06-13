import os
from flask import Flask, render_template, redirect, request, url_for
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
    return render_template("home.html")
    
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
            return redirect(url_for('add_user_success'))
    return render_template('signup.html', error=error)
        
@app.route('/sign_in_add')
def sign_in_add():
    return render_template('signinadd.html', error = "")
    
@app.route('/add_recipe', methods=["POST"])
def log_in():
    user = mongo.db.users.count({"$and": [{'username': request.form.get('username')}, {'password': request.form.get('password')}]})
    if request.method == 'POST':
        if user > 0:
            return render_template('addrecipe.html', user = user)
        else:
            error = "Sorry, your Username or Password is incorrect"
            return render_template('signinadd.html', error = error)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
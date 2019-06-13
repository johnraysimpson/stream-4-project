import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'cook_book'
app.config["MONGO_URI"] = 'mongodb+srv://jraysim:OrganD0NER@myfirstcluster-hdrnx.mongodb.net/cook_book?retryWrites=true&w=majority'

mongo = PyMongo(app)


@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html", user=mongo.db.users.find_one({'first': 'John'}))
    
@app.route('/sign_up')
def sign_up():
    return render_template('signup.html', error = "")
    
@app.route('/add_user', methods=["POST", "GET"])
def add_user():
    newuser = mongo.db.users.count({'username': request.form.get('username')})
    if newuser > 0 :
        return render_template('signup.html', error = "{0} has already been taken".format(request.form.get('username')))
    else:
        mongo.db.users.insert_one(request.form.to_dict())
        return render_template('signupsuccess.html')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
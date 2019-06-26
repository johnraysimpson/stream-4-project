import os
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_pymongo import PyMongo
import datetime
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
    return render_template('signup.html')

@app.route('/add_user/failed', methods=["POST", "GET"])
def add_user():
    newuser = mongo.db.users.count({'username': request.form.get('username')})
    if request.method == 'POST':
        if newuser > 0:
            error = "{0} has already been taken".format(request.form.get('username'))
        else:
            flash("Your account has been created, log in to continue")
            mongo.db.users.insert_one(request.form.to_dict())
            return redirect('sign_in')
    return render_template('signup.html', error=error)
        
@app.route('/sign_in')
def sign_in():
    return render_template('signin.html')
    
@app.route('/log_in/failed', methods=["POST"])
def log_in():
    users = mongo.db.users.find({'username': request.form.get('username'), 'password': request.form.get('password')})
    if request.method == 'POST':
        if users.count() > 0:
            user = mongo.db.users.find_one({'username': request.form.get('username'), 'password': request.form.get('password')})
        else:
            error = "Sorry, your Username or Password is incorrect"
            return render_template('signin.html', error = error)
    return redirect(url_for('user_home', user_id=user['_id']))
            
@app.route('/home/<user_id>')
def user_home(user_id):
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    return render_template('home.html', user=user)
    
@app.route('/add_recipe/<user_id>')
def add_recipe(user_id):
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    meal_types = mongo.db.meal_type.find()
    return render_template('addrecipe.html', user=user, meal_types=meal_types)
    
@app.route('/insert_recipe/<user_id>', methods=["POST", "GET"])
def insert_recipe(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    date_and_time = datetime.datetime.now()
    prep_time = int(request.form.get('prep_time'))
    cook_time = int(request.form.get('cook_time'))
    total_time = prep_time + cook_time
    if total_time >= 60 and total_time // 60 == 1:
        total_time_string = str(total_time // 60)+" hour "+ str(total_time % 60)+" minutes"
    elif total_time >= 60:
        total_time_string = str(total_time // 60)+" hours "+ str(total_time % 60)+" minutes"
    else:
        total_time_string = str(total_time)+" minutes"
    
    new_insert = {
        'username': request.form.get('username'),
        'country': request.form.get('country'),
        'meal_name': request.form.get('meal_name'),
        'prep_time': str(prep_time)+" minutes",
        'cook_time': str(cook_time)+" minutes",
        'meal_type': request.form.get('meal_type'),
        'date_and_time': date_and_time,
        'date_added': date_and_time.strftime("%d %B, %Y"),
        'favourite_count': 0,
        'meal_image': request.form.get('meal_image'),
        'total_time': total_time_string,
        'vegetarian': request.form.get('vegetarian'),
        'vegan': request.form.get('vegan'),
        'gluten_free': request.form.get('gluten_free'),
    }
    
    allergen_results = {
        'celery': request.form.get('celery'),
        'gluten': request.form.get('gluten'),
        'crustaceans': request.form.get('crustaceans'),
        'egg': request.form.get('egg'),
        'fish': request.form.get('fish'),
        'lupin': request.form.get('lupin'),
        'milk': request.form.get('milk'),
        'molluscs': request.form.get('molluscs'),
        'mustard': request.form.get('mustard'),
        'nuts': request.form.get('nuts'),
        'peanuts': request.form.get('peanuts'),
        'sesame_seeds': request.form.get('sesame_seeds'),
        'soya': request.form.get('soya'),
        'sulpher_dioxide': request.form.get('sulpher_dioxide')
    }
    allergens = {}
    for allergen in allergen_results:
        if allergen_results[allergen] != None:
            allergens.update({allergen: allergen_results[allergen]})
    new_insert.update({'allergens': allergens})
    ingredients = {}
    methods = {}
    for x in range(1, 21):
        ingredient_name = 'ingredient['+str(x)+']'
        if request.form.get("amount["+str(x)+"]") != None:
            if request.form.get("amount["+str(x)+"]").isdigit():
                if request.form.get("prep["+str(x)+"]") == "":
                    ingredient_value = ("%s %s" %(request.form.get("amount["+str(x)+"]"), request.form.get("ingredient["+str(x)+"]")))
                    ingredients.update({ingredient_name: ingredient_value})
                else:
                    ingredient_value = ("%s %s (%s)" %(request.form.get("amount["+str(x)+"]"), request.form.get("ingredient["+str(x)+"]"), request.form.get("prep["+str(x)+"]")))
                    ingredients.update({ingredient_name: ingredient_value})
            elif request.form.get("prep["+str(x)+"]") == "":
                ingredient_value = ("%s of %s" %(request.form.get("amount["+str(x)+"]"), request.form.get("ingredient["+str(x)+"]")))
                ingredients.update({ingredient_name: ingredient_value})
            else:
                ingredient_value = ("%s of %s (%s)" %(request.form.get("amount["+str(x)+"]"), request.form.get("ingredient["+str(x)+"]"), request.form.get("prep["+str(x)+"]")))
                ingredients.update({ingredient_name: ingredient_value})
    for x in range(1, 11):
        method_step = 'method_step['+str(x)+']'
        if request.form.get("method["+str(x)+"]") != None:
            method_value = request.form.get("method["+str(x)+"]")
            methods.update({method_step: method_value})
    new_insert.update({'ingredients': ingredients})
    new_insert.update({'methods': methods})
    mongo.db.recipes.insert_one(new_insert)
    return redirect(url_for("get_user_recipes", user_id = user_id))
    
@app.route('/my_recipes/<user_id>')
def get_user_recipes(user_id):
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    user_recipes = mongo.db.recipes.find_one({'username': user['username']})
    ingredients = user_recipes.get("ingredients")
    print(ingredients)
    return render_template('myrecipes.html', user_recipes=user_recipes, user=user, ingredients=ingredients)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
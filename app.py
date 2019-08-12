import os
from flask import Flask, render_template, redirect, request, url_for, flash
from pymongo import MongoClient
from flask_pymongo import PyMongo
import datetime
from bson.objectid import ObjectId
import json
from bson import json_util
from bson.json_util import dumps
import math



result = ""

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config["MONGO_DBNAME"] = 'cook_book'
app.config["MONGO_URI"] = os.getenv('MONGO_URI')

mongo = PyMongo(app)


@app.route('/')
@app.route('/home')
def home_not_user():
    popular_recipes = mongo.db.recipes.find().sort('favourite_count', -1).limit(5)
    new_recipes = mongo.db.recipes.find().sort('date_and_time', -1).limit(5)
    return render_template("home.html", popular_recipes=popular_recipes, new_recipes=new_recipes)
    

@app.route('/home/<user_id>')
def home(user_id):
    popular_recipes = mongo.db.recipes.find().sort('favourite_count', -1).limit(5)
    new_recipes = mongo.db.recipes.find().sort('date_and_time', -1).limit(5)
    if user_id != '0':
        user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        return render_template('home.html', user=user, popular_recipes=popular_recipes, new_recipes=new_recipes)
    else:
        return render_template("home.html", popular_recipes=popular_recipes, new_recipes=new_recipes)
    
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
            return redirect(url_for('sign_in'))
    return render_template('signup.html', error=error)
        
@app.route('/sign_in')
def sign_in():
    return render_template('signin.html')
    
@app.route('/log_in/failed', methods=["POST"])
def log_in():
    users = mongo.db.users.find({'username': request.form.get('username').lower(), 'password': request.form.get('password')})
    if request.method == 'POST':
        if users.count() > 0:
            user = mongo.db.users.find_one({'username': request.form.get('username').lower(), 'password': request.form.get('password')})
        else:
            error = "Sorry, your Username or Password is incorrect"
            return render_template('signin.html', error = error)
    return redirect(url_for('home', user_id=user['_id']))
    
@app.route('/sign_out')
def sign_out():
    return redirect(url_for('home', user_id='0'))
    
@app.route('/add_recipe/<user_id>')
def add_recipe(user_id):
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    meal_types = mongo.db.meal_type.find().sort('id')
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
    if int(request.form.get('serves')) == 1:
        serves = request.form.get('serves') + " person"
    else:
        serves = request.form.get('serves') + " people"
    
    new_insert = {
        'username': user['username'],
        'country': user['country'],
        'meal_name': request.form.get('meal_name'),
        'prep_time': int(prep_time),
        'cook_time': int(cook_time),
        'total_time': int(total_time),
        'meal_type': request.form.get('meal_type'),
        'date_and_time': date_and_time,
        'date_added': date_and_time.strftime("%d %B, %Y"),
        'favourite_count': 0,
        'total_time_string': total_time_string,
        'vegetarian': request.form.get('vegetarian'),
        'vegan': request.form.get('vegan'),
        'gluten_free': request.form.get('gluten_free'),
        'meal_desc': request.form.get('meal_desc'),
        'serves': serves,
        'serves_int': request.form.get('serves'),
        'favourited_users': {}
        
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
    
    for x in range(1, 21):
        ingredient_name = 'ingredient['+str(x)+']'
        if request.form.get("amount["+str(x)+"]") != None:
            if request.form.get("amount["+str(x)+"]").isdigit():
                if request.form.get("prep["+str(x)+"]") == "":
                    ingredient_value = ("%s %s" %(request.form.get("amount["+str(x)+"]"), request.form.get("ingredient["+str(x)+"]").lower()))
                    ingredients.update({ingredient_name: ingredient_value})
                else:
                    ingredient_value = ("%s %s (%s)" %(request.form.get("amount["+str(x)+"]"), request.form.get("ingredient["+str(x)+"]").lower(), request.form.get("prep["+str(x)+"]").lower()))
                    ingredients.update({ingredient_name: ingredient_value})
            elif request.form.get("prep["+str(x)+"]") == "":
                ingredient_value = ("%s of %s" %(request.form.get("amount["+str(x)+"]").capitalize(), request.form.get("ingredient["+str(x)+"]").lower()))
                ingredients.update({ingredient_name: ingredient_value})
            else:
                ingredient_value = ("%s of %s (%s)" %(request.form.get("amount["+str(x)+"]").capitalize(), request.form.get("ingredient["+str(x)+"]").lower(), request.form.get("prep["+str(x)+"]").lower()))
                ingredients.update({ingredient_name: ingredient_value})
    
    methods = {}
    
    for x in range(1, 11):
        method_step = 'method_step['+str(x)+']'
        if request.form.get("method["+str(x)+"]") != None:
            method_value = request.form.get("method["+str(x)+"]").capitalize()
            methods.update({method_step: method_value})
    new_insert.update({'ingredients': ingredients})
    new_insert.update({'methods': methods})
    mongo.db.recipes.insert_one(new_insert)
    return redirect(url_for("get_user_recipes", user_id = user_id))
    
@app.route('/my_recipes/<user_id>')
def get_user_recipes(user_id):
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    user_recipes = mongo.db.recipes.find({'username': user['username']})
    return render_template('myrecipes.html', user_recipes=user_recipes, user=user)
    
@app.route('/recipe/<recipe_id>/<user_id>')
def view_recipe(recipe_id, user_id):
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    if user_id != '0':
        user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        return render_template('recipe.html', recipe=recipe, user=user)
    else:
        return render_template('recipe.html', recipe=recipe)
    
@app.route('/edit_recipe/<recipe_id>/<user_id>')
def edit_recipe(recipe_id, user_id):
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    meal_types = mongo.db.meal_type.find().sort('_id')
    return render_template('editrecipe.html', recipe=recipe, user=user, meal_types=meal_types)
    
@app.route('/update_recipe/<recipe_id>/<user_id>', methods=["POST", "GET"])
def update_recipe(recipe_id, user_id):
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    
    prep_time = int(request.form.get('prep_time'))
    cook_time = int(request.form.get('cook_time'))
    total_time = prep_time + cook_time
    
    if total_time >= 60 and total_time // 60 == 1:
        total_time_string = str(total_time // 60)+" hour "+ str(total_time % 60)+" minutes"
    elif total_time >= 60:
        total_time_string = str(total_time // 60)+" hours "+ str(total_time % 60)+" minutes"
    else:
        total_time_string = str(total_time)+" minutes"
    if int(request.form.get('serves')) == 1:
        serves = request.form.get('serves') + " person"
    else:
        serves = request.form.get('serves') + " people"
    
    update_insert = {
        'meal_name': request.form.get('meal_name'),
        'prep_time': int(prep_time),
        'cook_time': int(cook_time),
        'total_time': int(total_time),
        'meal_type': request.form.get('meal_type'),
        'total_time_string': total_time_string,
        'vegetarian': request.form.get('vegetarian'),
        'vegan': request.form.get('vegan'),
        'gluten_free': request.form.get('gluten_free'),
        'meal_desc': request.form.get('meal_desc'),
        'serves': serves,
        'serves_int': request.form.get('serves')
        
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
    update_insert.update({'allergens': allergens})
    
    ingredients = {}
    
    for x in range(1, 21):
        ingredient_name = 'ingredient['+str(x)+']'
        if request.form.get("ingredient["+str(x)+"]") != "":
            ingredient_value = request.form.get("ingredient["+str(x)+"]").capitalize()
            ingredients.update({ingredient_name: ingredient_value})
    
    methods = {}
    
    for x in range(1, 11):
        method_step = 'method_step['+str(x)+']'
        if request.form.get("method["+str(x)+"]") != "":
            method_value = request.form.get("method["+str(x)+"]").capitalize()
            methods.update({method_step: method_value})
    update_insert.update({'ingredients': ingredients})
    update_insert.update({'methods': methods})
    mongo.db.recipes.update({'_id': ObjectId(recipe_id)}, { "$set": update_insert })
    return redirect(url_for('view_recipe', user_id=user['_id'], recipe_id=recipe['_id']))
    
@app.route('/delete_recipe/<recipe_id>/<user_id>')
def delete_confirm(recipe_id, user_id):
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    return render_template('deleterecipe.html', user=user, recipe=recipe)
    
@app.route('/remove_recipe/<recipe_id>/<user_id>')
def delete_recipe(recipe_id, user_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for("get_user_recipes", user_id = user_id))
    
@app.route('/favourited/<recipe_id>/<user_id>', methods=["POST"])
def favourited(recipe_id, user_id):
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    
    mongo.db.recipes.update({'_id': ObjectId(recipe_id)},{"$set": {'favourite_count': int(int(recipe['favourite_count']) + 1)}})

    mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, {"$set": {"favourited_users."+user['username']: user['username']} })
    return redirect(url_for('view_recipe', recipe_id=recipe['_id'], user_id=user['_id']))
    
@app.route('/unfavourited/<recipe_id>/<user_id>', methods=["POST"])
def unfavourited(recipe_id, user_id):
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    
    mongo.db.recipes.update({'_id': ObjectId(recipe_id)},{"$set": {'favourite_count': int(int(recipe['favourite_count']) - 1)}})

    mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, {"$unset": {"favourited_users."+user['username']: user['username']} })
    return redirect(url_for('view_recipe', recipe_id=recipe['_id'], user_id=user['_id']))
    
@app.route('/my_favourites/<user_id>')
def get_favourite_recipes(user_id):
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    favourite_recipes = mongo.db.recipes.find({'favourited_users.'+user['username']: user['username']})
    return render_template('myfavourites.html', favourite_recipes=favourite_recipes, user=user)

@app.route('/search_results/<user_id>/page_<page>', methods=["POST", "GET"])
def search_recipes(user_id, page):
    page = page
    search_params = request.form.to_dict()
    print(search_params)
    filters = {'$text': {'$search': search_params['search']}}
    #time filter
    if 'time' in search_params:
        if search_params['time'] == 'time_30':
            filters.update({'total_time': {'$lte': 30}})
        elif search_params['time'] == 'time_30_60':
            filters.update({'total_time': {'$gt': 30, '$lt': 60}})
        elif search_params['time'] == 'time_over_60':
            filters.update({'total_time': {'$gte': 60}})
    #dietry filters
    diet_options = {'vegetarian', 'vegan', 'gluten_free'}
    for option in diet_options:
        if option in search_params:
            if search_params[option]:
                filters.update({option: 'on'})
    #allergen filters
    allergens = {
        'celery', 'gluten', 'crustaceans','egg', 'fish', 'lupin', 
        'milk', 'molluscs', 'mustard', 'nuts', 'peanuts', 'sesame_seeds',
        'soya', 'sulpher_dioxide'
    }
    for allergen in allergens:
        if allergen in search_params:
            if search_params[allergen]:
                filters.update({'allergens.'+allergen+'': {'$exists': False}})
    #meal type filters
    meal_types = mongo.db.meal_type.find()
    for meal_type in meal_types:
        if 'meal_type' in search_params:
            if meal_type['meal_type'] == search_params['meal_type']:
                filters.update({'meal_type': search_params['meal_type']})
    #find based on applied filters
    found_recipes = mongo.db.recipes.find(filters).sort('favourite_count', -1)
    meal_types = mongo.db.meal_type.find().sort('_id')
    #sort filter
    if request.form.get('sort_by') == 'newest':
        found_recipes = found_recipes.sort('date_and_time', -1)
        
    number_of_recipes = found_recipes.count()
    number_of_pages = math.ceil(number_of_recipes/10)
    found_recipes = found_recipes.skip(int(page)*10-10).limit(10)
    if user_id != '0':
        user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        return render_template('searchresults.html', found_recipes=found_recipes, number_of_pages=number_of_pages, filters=filters, number_of_recipes=number_of_recipes, search_params=search_params, meal_types = meal_types, page=page, user=user)
    else:
        return render_template('searchresults.html', found_recipes=found_recipes, number_of_pages=number_of_pages, filters=filters, number_of_recipes=number_of_recipes, search_params=search_params, meal_types = meal_types, page=page)

    
@app.route('/analytics/<user_id>')
def analytics(user_id):
    if user_id != '0':
        user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        return render_template('analytics.html', user = user)
    else:
        return render_template('analytics.html')
    
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'cook_book'
COLLECTION_NAME = 'recipes'
    
@app.route("/cook_book/recipes")
def recipes_data():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    recipes = mongo.db.recipes.find()
    json_recipes = []
    for recipe in recipes:
        json_recipes.append(recipe)
    json_recipes = json.dumps(json_recipes, default=json_util.default)
    connection.close()
    return json_recipes


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
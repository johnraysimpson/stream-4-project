# Stream Four Project - Recipe Website

Cooking is a passion that many people - including myself - enjoy as it gives an individual gratification when putting smiles on the faces of friends and family after cooking a homely meal well. People often want to share their creativity with cooking, particularly online, 
which is the aim of this project. This site allows users to create an account, add their own recipes, make changes to those recipes and create a 'virtual cookbook' by favouriting recipes they have found and want to cook again. Users, with an account or not, can also search 
for recipes based on a keyword, perhaps an ingredient they are not sure what to do with.

## UX

This website is aimed towards a two types of users:

* Passionate people who wish to share, develop and take inspiration from recipes.
* Casual people who want to find something quick and easy to cook one evening.

Both of these types are fully catered for. For the casual user, they are able to see popular and new recipes on the homepage, as well as search for recipes dependent on keywords and from there filter their results very accurately in terms of timing, the type of meal, 
dietary requirements such as vegetarian, and allergens. They can choose a recipe to view, which gives them further information such as the user who created it, the country it is from and of course, the ingredients and method steps.

The passionate users also have access to this, but may choose to create an account on the Sign Up page and login to the site on the Sign In page. If done successfully, they remain signed in unless they close the page or choose to clickthe Sign Out button in the 
navigation bar. They are able to add their own recipes, which can then be viewed by other users. The ingredients fields are particular to ensure all ingredients look the same on any recipe i.e. "amount ingredient (preperation)". Universally, an asterisk is used to 
show where a field is required so I used these for the users information. They can then edit the recipe if they have made any mistakes or improvements, particularly with the ingredients, these appear as text fields instead. They can also delete the recipe completely 
if they choose to. If the user particularly likes a recipe, they can choose to 'favourite' the recipe which will add that recipe to a new page called Favourites. The user can then come back to that recipe easily, rather than having to search for it, creating a 
'virtual cookbook' - a bank of recipes for them to use again.

There is also an analytics page which shows pie charts representing the proportions of types of meal, the length of time it takes to cook a recipe and the country of origin. These can be filtered by clicking the slices, for example, you may want to see the proportions 
for length of time for main meals only.

Wireframes and mockups can be found in the corresponding folder of this project.

## Features

### Existing Features

Non-user features

* Searching - allows all users to search recipes based on a keyword.
* Search filtering - allows all users to concentrate their search results to their specific needs.
* Recipe view - allows all users to see the details of the recipe, including the ingredients and method steps. These can be shown and hidden at any time using the Materialize Collapsible JavaScript feature.
* Sign up page - a form that passionate users can use to create an account on the site.
* Sign in page - allows passionate users with an account to sign into it, users who have successfully created an account are redirected to this page and prompted to sign in using a flashed message.
* Data analytics page - allows users to view represented data in the form of pie charts for type of meal, time and country of origin. Each slice is clickable to filter information.

User features (once signed in)

* Add recipe page - a form where passionate users can add their own recipes for others to view.
* My recipes page - an area where passionate users can view, edit or delete their recipes.
* Edit recipe page - a form which uses the information of the recipe to replicate the entries, which users can edit and resend.
* Delete recipe page - when chosen, the user is asked if they definitely want to delete the recipe. They can choose either to go back to My Recipes page or delete the recipe permenantly.
* View recipe page - Similar for any user, however the passionate user can choose to add a recipe to their favourites, or remove a recipe already in their favourites.
* Favourites page - an area where passionate users can view all the recipes they have favourited.
* Sign out button - a user can choose to sign out of their account, although they will be once the page has closed.

### Features left to implement

* A safer account creation process would make this site more secure, I have included a message on the sign up page for users not to use a password they regularly use just in case.
* Pictures of the meals would have been nice, however upon researching this I found I would need tomake use of GridFS. With more time this may have been a useful implement.
* A more concise method of searching, my application currently uses the full text search `$text`. Although this works, you can search 'june' and get all the recipes created in June. I know the operator `$regex` can be used to do this and I may use that in future.

## Technologies used

* HTML5
    * all files found in templates folder
* CSS3
    * for styling purposes, found in static folder
* Materialize CSS and JS 1.0.0
    * for navigation bar, footer, forms, styling and grids.
* Material Icons
    * for visualisation and information.
* jQuery
    * in the files of the templates folder where necessary, for dropdown buttons, adding fields to form and materialize components
* Analytical JS
    * For data representation, includes:
        * D3 3.5.17
        * DC 2.1.8
        * Crossfilter 1.3.12
        * Queue 1.0.7
* Python
    * For backend development, imported libraries include:
        * Flask
        * Jinja
        * pyMongo
        * datetime
        * bson
        * json
        * math
* MongoDB
    * for documenting user information, recipe information and types of meals.

## Testing

Sign up form
* tried empty fields to check required attributes were working and error message appears.
* tried to use a username that exists in database, an error message appears and if all other information is retained if it is taken.
* tried to use a password that is less than 6 characters to check error message appears.
* tried to use a different password in the confirm password field to check error message appears.
* tested country autocomplete functionality.
* tried to input information correctly to see if it was successful, checked flash message works when redirected to sign in and made sure entry was made in database.

Sign in form
* tried empty fields to check required attributes were working and error message appears.
* used right username wrong password, wrong username wrong password, wrong username right password to check if error message appears and redirected to same page and entered username is retained.
* tried to input information correctly to see if it was successful and redirected properly.

Add recipe form
* tried empty fields to check required attributes were working and error message appears.
* tried to type letters in number fields
* tried to exceed character count on meal description
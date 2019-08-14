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
* Pictures of the meals would have been nice, however upon researching this I found I would need to make use of GridFS. With more time this may have been a useful implement.
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
* tried to exceed character count on meal description and meal name to check if they work properly.
* looked at type of meal field to see if those are being retrieved from MongoDB correctly.
* tested functionality of buttons to add new fields and they work appropriately, used google chrome developer tools to check HTML code.
* tried a range of different inputs to see if they are sent to MongoDB correctly, particularly for the coding for how the ingredients are used and written after posting.

Edit recipe form
* checked to see if correct information was being returned and in the correct fields.
* very similar form to the add recipe form so many of the same tests were done.

Delete recipe request
* checked to see if the user is redirected to the correct confirmation page with the correct information about the recipe.
* tried to delete recipe and checked to see if it was removed from the database.

Recipe page
* checked information loaded correctly
* tested the collapsible element, and making the accordion effect false.

Nav bar
* tested dropdown function works.
* tested mobile view works.
* tested all links take you to appropriate pages.

Data analytics
* checked the pie charts represent the correct data.
* checked my code for center alignment works.

Search form
* tried to enter a term that doesn't exist in data to see if 0 results.
* tried to enter a term in all recipes to see if all results are returned.
* tried to enter specific terms to see if one or two results are returned.
* tested a range of combinations of filters to check if they work correctly.
* tested pagination for just 2 results per page, increased this to 10.

Mobile responsiveness
* tested all pages to ensure they look good on all screen widths.

## Deployment

The files in this project have been pushed to my GitHub repository and can be found here https://github.com/johnraysimpson/stream-4-project Each git commit had a meaningful message describing the changes and happened frequently.
The app has been deployed to Heroku using the CLI and can be found here https://cook-book-project-db.herokuapp.com/
The config vars are in heroku so the app can only be seen there, these include:
* the MONGO_URI
* a SECRET_KEY
* the PORT
* the IP
To run the code locally these values would need to be used in the app.py file.

## Credits

Links used to help with any areas I found difficult
* jinja methods documentation - http://jinja.pocoo.org/docs/2.10/templates/#builtin-filters
* information about values and keys - https://stackoverflow.com/questions/44619572/join-the-values-only-in-a-python-dictionary
* very helpful resource to use MongoDB information for data visualisation - http://adilmoujahid.com/posts/2015/01/interactive-data-visualization-d3-dc-python-mongodb/
* implementing "add fields" buttons to add recipe page - https://www.allphptricks.com/add-remove-input-fields-dynamically-using-jquery/

The rest of the code was written by myself, I felt I've come a long way and Python really made sense to me. Hopefully a lot of the code throughout this project shows that.

Media
* vegetarian mark was found here - http://vegetarianmark.net/
* Vegan symbol was found here - https://868estatevineyards.com/visit/the-grill/vegan-symbol/
* Gluten free symbol found here - https://github.com/FortAwesome/Font-Awesome/issues/15304

Acknowledgements
* Big thanks to my partner, who has a surplus amount of recipe books and has a wide knowledge of recipe websites. It helped immensely when making this project.
* Many thanks goes to the slack community, they were very helpful, particularly with the movement to Amazon Web Services.
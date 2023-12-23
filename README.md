# Welcome to African Cuisines Recipes Api
***

## Task
Build a backend project providing an API, document and host it on the web.

## Description
### African Cuisines Recipe Restful API
A RESTFUL API that provides detailed information about African cuisines. As well as step by step instructions on how to make them. The API features a GraphQL endpoint, Swagger documentation, Postman documentation and RESTFUL API endpoints.

Authentication is done using API Key for protected route.

## Project Links

- [API Endpoints](https://acr-api.mikerock.tech/api/v1/status)
- [Swagger Documentation](https://acr-api.mikerock.tech/api/v1/docs)
- [GraphQL Endpoint](https://acr-api.mikerock.tech/api/v1/graphql)
- [Postman Documentation](https://documenter.getpostman.com/view/30168355/2s9YJf126k)



## Installation
#### In the root directory of the project
1. Install python and project dependencies and packages
```bash
$ sudo apt update
$ sudo apt install -y python3
$ sudo apt install -y python3-pip
$ sudo apt install -y python3-venv
$ sudo apt-get install -y pkg-config
$ sudo apt-get install -y libmysqlclient-dev
$ sudo apt install -y nginx
$ pip install gunicorn
$ sudo apt install redis-server
$ sudo apt install mysql-server
$ sudo systemctl start mysql.service
$ pip install -r requirements.txt
```
2. Setup database
```bash
$ cat setupDatabase.sql | mysql
```
3. Setup virtual environment
```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```
4. Start the API servers
```bash
$ bash start_servers
```
5. The RESTFUL API will be running on http://localhost:9000/api/v1/status while the graphql api on http://localhost:9000/api/v1/graphql and the swagger documentation on http://localhost:9001/api/v1/docs


## Usage
1. Create a user account POST /users
2. Login to get your authentication token POST /login
3. Create a recipe on POST /recipes
4. Update a recipe on PUT /recipes/{id}
5. Delete your recipe on DELETE /recipes/{id}
6. Get a list of all available recipes on GET /recipes
7. Search a recipe by querying GET /recipes?search=Plantain
8. Data is paginated 10 items per page. You can specify a page to fetch by passing it in the query (e.g. GET /recipes?page=4)
9. You can filter recipes by adding a dictionary of key(string), value(array containing filter values) in your query parameter. (Example : { "cuisine": [ "Nigerian", "West African", "Ghanaian" ], "cook_time_minutes": [ 6, 10, 50 ] })
10. Destroy user session by querying the DELETE /logout
11. Update user by querying PUT /users/{id}
12. Delete user by querying DELETE /users/{id}


```bash
$ curl localhost:9000/api/v1/recipes
```
## Endpoints

Users
GET
​/api​/v1​/users
Retrieves a list of all users.
get_api_v1_users
Parameters
Name	Description
detailed
(query)
	

Set to true to see full user information
Responses
Response content type
Code	Description
200	

Successfully fetched users
401	

Only admins can view this route
POST
​/api​/v1​/users
Creates a new user
post_api_v1_users
GET
​/api​/v1​/users​/me
Retrieves a the current user information.
get_api_v1_users_me
GET
​/api​/v1​/users​/{id}
Retrieves a user based on id.
get_api_v1_users__id_
PUT
​/api​/v1​/users​/{id}
Updates a user based on ID
put_api_v1_users__id_
DELETE
​/api​/v1​/users​/{id}
Deletes a user based on ID
delete_api_v1_users__id_
PUT
​/api​/v1​/users​/dp
Upload and Update User's Display Picture
put_api_v1_users_dp
GET
​/api​/v1​/users​/dp​/{userID}
Retrieves the current users display picture file
get_api_v1_users_dp__userID_

Sessions
POST
​/api​/v1​/login
Validates user and creates a user session
post_api_v1_login
Parameters
Name	Description
Login Data *
object
(body)
	

Login credentials

    Example Value
    Model

{
  "email": "mikerock@email.com",
  "password": "password"
}

Parameter content type
detailed
(query)
	

Set to true to see full user information
Responses
Response content type
Code	Description
200	

Login successful
400	

Not a JSON data || One or more required fields missing || Incorrect email or password
404	

User does not exist
DELETE
​/api​/v1​/logout
Destroys user session
delete_api_v1_logout

Recipes
GET
​/api​/v1​/recipes
Retrieves a paginated list of all recipes (10 recipes per page).
get_api_v1_recipes
Parameters

## Examples 


Name	Description
page
(query)
	

(Optional) Page to fetch (1 page <= 10 items). Fetches the first page if no value is provided.
search
(query)
	

Search recipe by name. (Optional)

Example : Ofe Akwu
filter_by
(query)
	

(Optional) Enter one or more filter criteria. Format is a dictionary with the filter field as key and an array of values.

Example : OrderedMap { "cuisine": List [ "Nigerian", "West African", "Ghanaian" ], "cook_time_minutes": List [ 6, 10, 50 ] }
detailed
(query)
	

Set to true to see full recipe information (Optional)
Responses
Response content type
Curl
curl -X GET "https://acr-api.mikerock.tech/api/v1/recipes" -H "accept: application/json"
Request URL

https://acr-api.mikerock.tech/api/v1/recipes

Server response
Code	Details
200	
Response body
Download

{
  "status": "success",
  "message": "Successfully fetched recipes",
  "page": 1,
  "page_size": 10,
  "total_page_items": 10,
  "total_pages": 104,
  "data": [
    {
      "name": "Malagasy Akoho Sy Voanio with Rice",
      "cuisine": "Malagasy",
      "id": "006dac12-423f-4a72-bcea-08cf35f44e7a",
      "prep_time_minutes": 20,
      "cook_time_minutes": 45,
      "total_time_minutes": 65,
      "calories_per_serving": 550,
      "serving_size": 4,
      "ingredients": [
        "2 pounds chicken, cut into pieces",
        "2 cups rice",
        "2 onions, chopped",
        "2 cloves garlic, minced",
        "2 tomatoes, chopped",
        "2 tablespoons vegetable oil",
        "1/2 cup coconut milk",
        "1/2 teaspoon ground cloves",
        "Salt and pepper to taste"
      ],
      "instructions": [
        "In a large pot, heat vegetable oil over medium-high heat. Add chopped onions and minced garlic. Sauté until onions are translucent.",
        "Stir in chopped tomatoes and cook until they soften.",
        "Add chicken pieces and cook until they are browned.",
        "Season with ground cloves, salt, and pepper. Mix well.",
        "Add coconut milk and enough water to cook the chicken. Simmer for about 20-25 minutes, or until the chicken is cooked through and tender.",
        "Prepare rice according to package instructions.",
        "Serve the Akoho Sy Voanio with Rice. Enjoy your Malagasy meal!"
      ],
      "dps": [
        {
          "fileType": "link",
          "id": "bdb60685-2e99-4a6b-a161-a8382aa09c4c",
          "createdAt": "2023-12-09T05:55:18",
          "userID": "4f0364a3-f82f-489e-8e02-8845b2ce7caa",
          "updatedAt": "2023-12-09T05:55:18",
          "filePath": "https://icons.iconarchive.com/icons/mcdo-design/closed-notes/256/Diary-Recipe-icon.png",
          "recipeID": "006dac12-423f-4a72-bcea-08cf35f44e7a"
        }
      ]
    },
    {
      "name": "Ivorian Kedjenou with Attieke",
      "cuisine": "Ivorian",
      "id": "007949bc-776d-4336-a0c6-ab164b91af06",
      "prep_time_minutes": 20,
      "cook_time_minutes": 40,
      "total_time_minutes": 60,
      "calories_per_serving": 380,
      "serving_size": 4,
      "ingredients": [
        "4 chicken drumsticks",
        "2 onions, chopped",
        "2 tomatoes, chopped",
        "2 eggplants, diced",
        "2 bell peppers, sliced",
        "2 habanero peppers, whole",
        "1/4 cup palm oil",
        "1/4 cup chicken broth",
        "2 tablespoons ginger, minced",
        "2 tablespoons garlic, minced",
        "2 bay leaves",
        "1 teaspoon thyme",
        "Salt and pepper to taste",
        "Cooked attieke for serving"
      ],
      "instructions": [
        "In a large pot, heat palm oil over medium heat. Add chopped onions, minced ginger, and minced garlic. Sauté until onions become translucent.",
        "Add chicken drumsticks and brown them on all sides.",
        "Stir in chopped tomatoes, diced eggplants, sliced bell peppers, and habanero peppers. Cook for a few minutes.",
        "Add bay leaves, thyme, salt, and pepper. Pour in chicken broth.",
        "Cover the pot and simmer over low heat for about 30 minutes, until the chicken is tender and the vegetables are cooked through.",
        "Serve Ivorian Kedjenou with cooked attieke for a traditional Ivorian meal."
      ],
      "dps": [
        {
          "fileType": "link",
          "id": "546294b4-e9e6-4b21-ad8b-b3b64e4c27a7",
          "createdAt": "2023-12-09T06:01:30",
          "userID": "4f0364a3-f82f-489e-8e02-8845b2ce7caa",
          "updatedAt": "2023-12-09T06:01:30",
          "filePath": "https://icons.iconarchive.com/icons/mcdo-design/closed-notes/256/Diary-Recipe-icon.png",
          "recipeID": "007949bc-776d-4336-a0c6-ab164b91af06"
        }
      ]
    },
    {
      "name": "Ethiopian Kitfo",
      "cuisine": "East African",
      "id": "00fe4aea-bae1-4e63-a0f8-8f6ee17ced04",
      "prep_time_minutes": 15,
      "cook_time_minutes": 0,
      "total_time_minutes": 15,
      "calories_per_serving": 300,
      "serving_size": 4,
      "ingredients": [
        "1 pound of beef sirloin, finely minced",
        "1/4 cup of niter kibbeh (spiced clarified butter)",
        "1/4 cup of mitmita spice blend (chili powder, cardamom, cloves, and other spices)",
        "Salt to taste",
        "Injera or flatbread for serving"
      ],
      "instructions": [
        "In a bowl, combine finely minced beef sirloin, niter kibbeh (spiced clarified butter), mitmita spice blend, and salt. Mix well.",
        "Serve the Ethiopian Kitfo raw, with injera or flatbread for scooping and wrapping the spiced beef."
      ],
      "dps": [
        {
          "fileType": "link",
          "id": "283c8bb7-2333-4bd8-9686-dc52875da144",
          "createdAt": "2023-12-09T05:37:02",
          "userID": "4f0364a3-f82f-489e-8e02-8845b2ce7caa",
          "updatedAt": "2023-12-09T05:37:02",
          "filePath": "https://icons.iconarchive.com/icons/mcdo-design/closed-notes/256/Diary-Recipe-icon.png",
          "recipeID": "00fe4aea-bae1-4e63-a0f8-8f6ee17ced04"
        }
      ]
    },
    {
      "name": "Cameroonian Ndole Soup with Bobolo",
      "cuisine": "Cameroonian",
      "id": "011273ef-c6e4-4f75-9fe2-7bd37865f261",
      "prep_time_minutes": 20,
      "cook_time_minutes": 35,
      "total_time_minutes": 55,
      "calories_per_serving": 400,
      "serving_size": 4,
      "ingredients": [
        "2 cups groundnut paste (peanut butter)",
        "1/2 cup palm oil",
        "1/2 cup crayfish, ground",
        "2 cups bitterleaf (substitute spinach if unavailable), washed and chopped",
        "2 cloves garlic, minced",
        "1 onion, chopped",
        "2 cups water",
        "Salt and pepper to taste",
        "Bobolo (fermented cassava bread) for serving"
      ],
      "instructions": [
        "In a pot, heat palm oil over medium-high heat. Add chopped onions and minced garlic. Sauté until onions are translucent.",
        "Stir in groundnut paste (peanut butter) and cook for a few minutes.",
        "Add ground crayfish and continue to cook.",
        "Pour in water and simmer for about 15-20 minutes.",
        "Add chopped bitterleaf (or spinach) and cook until it's tender, about 10-15 minutes.",
        "Season with salt and pepper to taste.",
        "Serve the Ndole Soup with Bobolo. Enjoy your Cameroonian meal!"
      ],
      "dps": [
        {
          "fileType": "link",
          "id": "8f755824-2c41-46a7-846f-337e8ae014b6",
          "createdAt": "2023-12-09T05:54:44",
          "userID": "4f0364a3-f82f-489e-8e02-8845b2ce7caa",
          "updatedAt": "2023-12-09T05:54:44",
          "filePath": "https://icons.iconarchive.com/icons/mcdo-design/closed-notes/256/Diary-Recipe-icon.png",
          "recipeID": "011273ef-c6e4-4f75-9fe2-7bd37865f261"
        }
      ]
    },
    {
      "name": "Sudanese Kuindiong",
      "cuisine": "African",
      "id": "016155f8-ead1-48ff-b444-866af462f0b4",
      "prep_time_minutes": 10,
      "cook_time_minutes": 15,
      "total_time_minutes": 25,
      "calories_per_serving": 200,
      "serving_size": 4,
      "ingredients": [
        "2 cups corn flour",
        "1/2 cup water",
        "2 tablespoons clarified butter (samna)",
        "1/4 cup grated cheese (optional)",
        "Salt to taste"
      ],
      "instructions": [
        "In a bowl, combine corn flour and water. Mix to form a smooth, dough-like consistency.",
        "In a pot, heat clarified butter (samna) over low heat.",
        "Add the corn flour mixture to the pot and stir continuously until it thickens and starts to come away from the sides of the pot.",
        "Add grated cheese if desired and salt to taste. Continue to stir until the mixture is well combined and cooked through.",
        "Remove from heat and shape the cooked mixture into small cylindrical rolls or serve it as a flatbread.",
        "Serve the Sudanese Kuindiong as a simple yet delicious African dish."
      ],
      "dps": [
        {
          "fileType": "link",
          "id": "d9f2107d-1bcf-4c9c-9fd0-1b9d0aede197",
          "createdAt": "2023-12-09T05:37:52",
          "userID": "4f0364a3-f82f-489e-8e02-8845b2ce7caa",
          "updatedAt": "2023-12-09T05:37:52",
          "filePath": "https://icons.iconarchive.com/icons/mcdo-design/closed-notes/256/Diary-Recipe-icon.png",
          "recipeID": "016155f8-ead1-48ff-b444-866af462f0b4"
        }
      ]
    },
    {
      "name": "Malagasy Tsaramaso",
      "cuisine": "Malagasy",
      "id": "01d8260b-4038-4423-8d5a-92057c664e33",
      "prep_time_minutes": 20,
      "cook_time_minutes": 40,
      "total_time_minutes": 60,
      "calories_per_serving": 350,
      "serving_size": 4,
      "ingredients": [
        "1 cup rice flour",
        "1/2 cup grated coconut",
        "1/2 cup sugar",
        "1/2 teaspoon ground cinnamon",
        "1/2 teaspoon ground cloves",
        "1/2 teaspoon grated lemon zest",
        "1/2 cup water",
        "Banana leaves for wrapping (substitute with parchment paper if unavailable)"
      ],
      "instructions": [
        "In a mixing bowl, combine rice flour, grated coconut, sugar, ground cinnamon, ground cloves, and grated lemon zest.",
        "Gradually add water to the dry ingredients and mix until you have a smooth batter.",
        "Cut banana leaves into rectangles and briefly pass them over an open flame to make them more pliable and to remove any raw smell.",
        "Place a portion of the batter onto a banana leaf and fold it into a rectangular packet, sealing the edges securely. Repeat with the remaining batter.",
        "Steam the wrapped packets for about 30-40 minutes, or until the Tsaramaso is cooked through.",
        "Allow the Tsaramaso to cool before unwrapping and slicing into portions.",
        "Serve Malagasy Tsaramaso as a sweet snack or dessert.",
        "Enjoy!"
      ],
      "dps": [
        {
          "fileType": "link",
          "id": "33182631-49ee-4cc8-a4a2-5d4b71988a01",
          "createdAt": "2023-12-09T05:43:28",
          "userID": "4f0364a3-f82f-489e-8e02-8845b2ce7caa",
          "updatedAt": "2023-12-09T05:43:28",
          "filePath": "https://icons.iconarchive.com/icons/mcdo-design/closed-notes/256/Diary-Recipe-icon.png",
          "recipeID": "01d8260b-4038-4423-8d5a-92057c664e33"
        }
      ]
    }
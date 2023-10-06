# Welcome to My Api
***

## Task
Build a backend project providing an API, document and host it on the web.

## Description
### African Cuisines Recipe Restful API
A RESTFUL API that provides detailed information about African cuisines. As well as step by step instructions on how to make them. The API features a GraphQL endpoint, Swagger documentation, Postman documentation and RESTFUL API endpoints.

Authentication is done using API Key for protected route.



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
5. The RESTFUL API will be running on http://localhost:9000/api/v1/status while the graphql api on http://localhost:9000/api/v1/graphql and the swagger documentation on http://localhost:9000/api/v1/docs


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

### The Core Team
- Michael Adebayo OGTL Academy => <a href="https://github.com/MikeRock51">Github</a>,
<a href="https://twitter.com/Mike_Rock1">Twitter</a>,
<a href="https://www.linkedin.com/in/michael-adebayo-637507251/">LinkedIn</a>
<a href="mailto:mikerockmusic51@gmail.com">Email</a>
- [RESTFUL AP ENDPOINT](https://acr-api.mikerock.tech/api/v1/)
- [Swagger Documentation](https://acr-api.mikerock.tech/api/v1/docs)
- [GraphQL Endpoint](https://acr-api.mikerock.tech/api/v1/graphql)
- [Postman Documentation](https://recipes.mikerock.tech/api/v1/status)


<span><i>Made at <a href='https://qwasar.io'>Qwasar SV -- Software Engineering School</a></i></span>
<span><img alt='Qwasar SV -- Software Engineering School's Logo' src='https://storage.googleapis.com/qwasar-public/qwasar-logo_50x50.png' width='20px' /></span>

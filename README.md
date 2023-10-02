# Welcome to My Api
***

## Task
Build a backend project providing an API, document and host it on the web.

## Description
### African Cuisines Recipe Restful API
A RESTFUL API that provides detailed information about African cuisines. As well as step by step instructions on how to make them.



## Installation
#### In the root directory of the project
1. Install python and project dependencies
```bash
$ sudo apt install python3
$ sudo apt install python3-pip
$ sudo apt-get install pkg-config
$ sudo apt-get install libmysqlclient-dev
$ pip3 install -r requirements.txt
```
2. Install mysql and setup database table
```bash
$ sudo apt install mysql-server
$ sudo systemctl start mysql.service
$ cat setupDatabase.sql | mysql
```
3. Install redis
```bash
$ sudo apt install redis-server
```
4. Start the API server
```bash
$ python3 -m api.v1.app
```
5. The app will be running on http://localhost:9000/api/v1/


## Usage
1. Create a user account POST /users
2. Login to get your authentication token POST /login
3. Create a recipe on POST /recipes
4. Update a recipe on PUT /recipes/{id}
5. Delete your recipe on DELETE /recipes/{id}
6. Get a list of all available recipes on GET /recipes
7. Search a recipe by querying GET /recipes?search=Plantain
8. Data is paginated 5 items per page. You can specify a page to fetch by passing it in the query (e.g. GET /recipes?page=4)
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
- [Deployed Project](http://recipes.mikerock.tech:9000/api/v1/status)
- [Swagger Documentation](http://recipes.mikerock.tech:9000/api/v1/docs)
- [Postman Documentation](https://recipes.mikerock.tech:9000/api/v1/status)


<span><i>Made at <a href='https://qwasar.io'>Qwasar SV -- Software Engineering School</a></i></span>
<span><img alt='Qwasar SV -- Software Engineering School's Logo' src='https://storage.googleapis.com/qwasar-public/qwasar-logo_50x50.png' width='20px' /></span>

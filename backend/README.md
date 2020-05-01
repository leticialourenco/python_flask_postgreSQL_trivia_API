# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## API Reference

* Base URL: This application is hosted locally. The backend is hosted at `http://127.0.0.1:5000/`
* Authentication: This version does not require authentication or API keys.

### Error Handling

Errors are being returned as JSON in the following format
```
{   "success": False,
    "error": 400,
    "message": "bad request"
}
```

Implemented error codes and messages:

- 400 – bad request
- 404 – resource not found
- 422 – unprocessable

### Endpoints

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id:category_string key:value pairs. 
```
{   "categories":
    {   '1':"Science",
        '2':"Art",
        '3':"Geography",
        '4':"History",
        '5':"Entertainment",
        '6':"Sports"  
    }
}
```

GET '/questions'
- Fetches a dictionary of questions and categories 
- Request Arguments: None
- Returns a paginated list of question objects, category object and total questions
```
{   "categories": {
        "1":"Science",
        "2":"Art",
        "3":"Geography",
        "4":"History",
        "5":"Entertainment",
        "6":"Sports" },
    "questions":[
        {   "answer":"Apollo 13",
            "category":5,
            "difficulty":4,
            "id":2,
            "question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?" },
        {   "answer":"Tom Cruise",
            "category":5,
            "difficulty":4,
            "id":4,
            "question":"What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?" }],
    "total_questions":2,
    "success":true
}
```

GET '/categories/\<int:category_id>\/questions'
- Request Arguments: id of category for questions to be fetched from
- Returns a paginated list of question objects and total questions
```
{   "questions":[
    {   "answer":"George Washington Carver",
        "category":4,
        "difficulty":2,
        "id":12,
        "question":"Who invented Peanut Butter?" },
    {   "answer":"Scarab",
        "category":4,
        "difficulty":4,
        "id":23,
        "question":"Which dung beetle was worshipped by the ancient Egyptians?" }
    ],
    "success":true,
    "total_questions":2
}
```

POST '/questions'
- Request Arguments: search term
- Fetch questions that contain search term 
- Returns a paginated list of question objects and total questions

```
{   "questions":[
    {   "answer":"Uruguay",
        "category":6,
        "difficulty":4,
        "id":11,
        "question":"Which country won the first ever soccer World Cup in 1930?" }
    ],
    "success":true,
    "total_questions":1
}
```

DELETE '/questions/\<int:question_id>\'
- Request Arguments: id of question to be deleted
- Returns an object with id of deleted question 
```
{   
    "deleted":2,
    "success":true
}
```

POST '/questions/create'
- Request Arguments: json containing values that can be used to initialize question object
- Creates a new question using JSON request parameters.
- Returns an question object containing the created question values
```
{   "question":
    {   "answer":"Blood",
        "category":1,
        "difficulty":4,
        "id":45,
        "question":"Hematology is a branch of medicine involving the study of what?"
    },
    "success":true
}
```

POST '/quizzes'
- Request Arguments: json containing values for a quiz_category id and previous_question list 
- Returns either a question object containing a question different than the ones contained in provided previous_question or
- Returns success in case there's no questions not present in previous_question (indicating end of game)
```
{   "question":
    {   "answer":"Blood",
        "category":1,
        "difficulty":4,
        "id":45,
        "question":"Hematology is a branch of medicine involving the study of what?" },
    "success":true
}
```

### Testing
To run the tests:
If db already exists, run first
```
dropdb trivia_test
```
then, otherwise, run
```
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# helper function - handles pagination
def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  questions = [question.format() for question in selection]
  current_questions = questions[start:end]
  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  # setup CORS app - allowing all origins
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  # setup CORS headers
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  @app.route("/")
  # @cross_origin()
  def index():
    return jsonify({
      'success': True
    })

  @app.route('/categories', methods=['GET'])
  def get_categories():
    # get all categories and re-format the collection into a dictionary
    categories = Category.query.all()
    formatted_categories = {}
    for category in categories:
      formatted_categories[category.id] = category.type

    return jsonify({
      'success': True,
      'categories': formatted_categories,
      'total_categories': len(categories)
    })

  @app.route('/questions', methods=['GET'])
  def get_questions():
    # get all questions and use the pagination helper func to break
    # into blocks of content
    all_questions = Question.query.all()
    current_questions = paginate_questions(request, all_questions)
    total_questions = len(all_questions)

    # get all categories and re-format the collection into a dictionary
    categories = Category.query.all()
    formatted_categories = {}
    for category in categories:
      formatted_categories[category.id] = category.type

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': total_questions,
      'categories': formatted_categories
    })

  @app.route('/question/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter_by(id=question_id).one_or_none()

      if question is None:
        abort(404)

      question.delete()

      return jsonify({
        'success': True,
        'deleted': question_id
      })
    except:
      abort(422)

  @app.route('/add', methods=['POST'])
  def add_question():
    try:
      # get data from the form request
      data = request.get_json()
      # populate variables with retrieved information
      question_field = data['question']
      answer = data['answer']
      difficulty = data['difficulty']
      category = data['category']
      # assign values to create a Question objects
      question = Question(
        question=question_field, answer=answer,
        difficulty=difficulty, category=category
      )
      # insert new question into database
      question.insert()
      return jsonify({
        'success': True
      })
    except:
      abort(422)

  @app.route('/questions', methods=['POST'])
  def get_questions_by_search():
    # get body of request to retrieve search_term
    search_term = request.get_json()['searchTerm']

    # query questions filtered by search term
    questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

    # get questions and use the pagination helper func to break
    # into blocks of content
    current_questions = paginate_questions(request, questions)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(questions)
    })

  @app.route('/category/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):
    # get all questions that share the category_id
    questions = Question.query.filter_by(category=category_id).all()
    # setup pagination using the helper
    # function and store block of content under current questions
    current_questions = paginate_questions(request, questions)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(questions),
    })

  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    # get body of request to retrieve category and previous questions
    body = request.get_json()
    category = body['quiz_category']
    previous_questions = body['previous_questions']

    # loads all questions in case category is ALL
    # or filter it by category in case it has one
    if category['id'] == 0:
      questions = Question.query.all()
    else:
      questions = Question.query.filter_by(category=category['id']).all()

    question = {}
    used_question = True
    # loops until an unused question is provided or all questions have been used
    while used_question:
      # gets a random question
      question = questions[random.randrange(0, len(questions), 1)]

      # in case there's no previous_questions such as first iteration
      if not previous_questions:
        used_question = False
      else:
        # loop through the list of previous questions
        # check that it is within this list
        for quest in previous_questions:
          if quest != question.id:
            used_question = False
      # in case all questions have been used
      # it returns no question
      if len(previous_questions) == len(questions):
        return jsonify(({
          'success': True
        }))

    return jsonify({
      'success': True,
      'question': question.format()
    })

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

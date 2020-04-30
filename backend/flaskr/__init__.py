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

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

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

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

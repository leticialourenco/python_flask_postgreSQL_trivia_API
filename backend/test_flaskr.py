import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

class TriviaTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        pass

    def test_get_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertTrue(len(data['categories']))
        self.assertTrue(data['total_categories'])

        # check response message and its code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['total_questions'])

        # check response message and its code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_question(self):
        # manually create a question to later be deleted
        new_question = Question(question="1 + 1 = ?", answer="2", category="1", difficulty="1")
        new_question.insert()

        # get all questions before deleting a sample one
        all_questions = Question.query.all()
        num_questions_before = len(all_questions)

        # deletes an entry and save its response and data to later ensure no errors
        response = self.client().delete('/questions/{}'.format(new_question.id))
        data = json.loads(response.data)

        # get all questions after deleting a sample one
        all_questions = Question.query.all()
        num_questions_after = len(all_questions)

        # asserts that length of all questions has decreased by 1
        self.assertEqual(num_questions_before, (num_questions_after+1))

        # check that the right question was deleted
        self.assertEqual(data['deleted'], new_question.id)

        # check response message and its code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_add_question(self):
        # get all questions before adding a sample one
        all_questions = Question.query.all()
        num_questions_before = len(all_questions)

        # create a question to test
        new_question = {"question": "1 + 1 = ?", "answer": "2", "category": "1", "difficulty": 1}
        response = self.client().post('/questions/create', json=new_question)
        data = json.loads(response.data)

        # get all questions after adding a sample one
        all_questions = Question.query.all()
        num_questions_after = len(all_questions)

        # asserts that length of all questions has increased by 1
        self.assertEqual(num_questions_before, (num_questions_after-1))

        # delete created question
        self.client().delete('/questions/{}'.format(data['question']['id']))

        # check response message and its code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_questions_by_search(self):
        # send a post request with a search term
        response = self.client().post('/questions', json={'searchTerm': 'What'})
        data = json.loads(response.data)

        # check that there are results
        self.assertTrue(len(data['questions']))

        # check response message and its code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_questions_by_category(self):
        # send a request of category id=1
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)

        # check accuracy of response data
        self.assertTrue(data['questions'])
        self.assertEqual(data['current_category'], '1')

        # check response message and its code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_play_quiz_with_category(self):
        # send a request containing quiz_category and previous_questions
        quiz = {'quiz_category': {'id': 1, 'type': 'Science'}, 'previous_questions': [20]}
        response = self.client().post('/quizzes', json=quiz)
        data = json.loads(response.data)

        # check that the request returned a question of category 1 and not within the previous_questions list
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['category'], 1)
        self.assertNotEqual(data['question']['id'], 20)

        # check response message and its code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_play_quiz_with_all_category(self):
        # send a request containing quiz_category (0 for ALL categories) and previous_questions
        quiz = {'quiz_category': {'id': 0, 'type': 'ALL'}, 'previous_questions': [20]}
        response = self.client().post('/quizzes', json=quiz)
        data = json.loads(response.data)

        # check that the request returned a question and not within the previous_questions list
        self.assertTrue(data['question'])
        self.assertNotEqual(data['question']['id'], 20)

        # check response message and its code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

if __name__ == "__main__":
    unittest.main()
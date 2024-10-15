import unittest
from flask_testing import TestCase
from app import app, conn

class TestFlaskApp(TestCase):
    def create_app(self):
        # Set testing configuration for the Flask app
        app.config['TESTING'] = True
        return app

    def setUp(self):
        # Called before every test. You can use this to set up the database.
        self.conn = conn
        self.conn.execute('DELETE FROM word_sounds')  # Clear the table before testing
        self.conn.commit()

    def tearDown(self):
        # Called after every test. You can clean up the database here.
        self.conn.execute('DELETE FROM word_sounds')
        self.conn.commit()

    def test_add_word(self):
        # Test the /api/add-word endpoint
        response = self.client.post('/api/add-word', json={'word': 'test'})
        self.assertEqual(response.status_code, 200)

        # Check if the word was added
        cursor = self.conn.execute('SELECT word FROM word_sounds WHERE word = ?', ('test',))
        result = cursor.fetchone()
        self.assertIsNotNone(result)

    def test_find_similar_words(self):
        # Add some words to the database for testing
        self.conn.execute('INSERT INTO word_sounds (word, metaphone_code) VALUES (?, ?)', ('bat', 'B0'))
        self.conn.execute('INSERT INTO word_sounds (word, metaphone_code) VALUES (?, ?)', ('cat', 'C0'))
        self.conn.commit()

        # Test the /api/similar-words endpoint
        response = self.client.post('/api/similar-words', json={'word': 'bat'})
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertIn('cat', data['similar_words'])

if __name__ == '__main__':
    unittest.main()

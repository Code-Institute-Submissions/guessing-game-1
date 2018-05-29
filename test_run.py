import unittest
import run
import json
from string import ascii_uppercase

class TestRun(unittest.TestCase):
    
    def test_remove_articles_from_string(self):
        some_articles = "Please give me some water."
        an_article = "Please give me an ice cube."
        
        self.assertNotEqual(run.remove_articles('the'), 'the')
        self.assertNotEqual(run.remove_articles(some_articles), some_articles)
        self.assertNotEqual(run.remove_articles(an_article), an_article)
        
    def test_if_user_exist(self):
        with open('data/username.json', 'r') as user_data:
            user_data = json.load(user_data)
        
        self.assertTrue(run.if_user_exist(user_data, 'denis'))
        self.assertFalse(run.if_user_exist(user_data, 'Ben'))

if __name__ == '__main__':
    unittest.main()
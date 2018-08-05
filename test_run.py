import unittest
from utils import user_exist, remove_articles
import json
from string import ascii_uppercase

class TestRun(unittest.TestCase):
    
    def test_remove_articles_from_string(self):
        some_articles = "Please give me some water."
        an_article = "Please give me an ice cube."
        
        self.assertNotEqual(remove_articles('the'), 'the')
        self.assertNotEqual(remove_articles(some_articles), some_articles)
        self.assertNotEqual(remove_articles(an_article), an_article)
        
    def test_if_user_exist(self):
        with open('data/username.json', 'r') as user_data:
            user_data = json.load(user_data)
        
        self.assertTrue(user_exist(user_data, 'denis'))
        self.assertFalse(user_exist(user_data, 'Ben'))

if __name__ == '__main__':
    unittest.main()
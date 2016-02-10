import unittest
from selenium import webdriver
from config import WAIT


class BaseCase(unittest.TestCase):
    '''MiniUrl base testing class'''

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(WAIT)

    def tearDown(self):
        self.driver.close()

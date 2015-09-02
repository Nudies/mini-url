import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class MiniUrl(unittest.TestCase):
	
	def setUp(self):
		self.driver = webdriver.Firefox()
		self.driver.get('http://localhost:5000')

	def tearDown(self):
		self.driver.close()

	def test_can_submit_link(self):
		# User sees a text input, puts in a url
		self.assertIn('Mini URL', self.driver.title)
		self.assertIn('Recent links', self.driver.page_source) 
		input = self.driver.find_element_by_name('url')
		input.send_keys('http://selenium-python.readthedocs.org')
		input.send_keys(Keys.RETURN)
	
		# Shortened url appears below text input	
		result = self.driver.find_element_by_id('result')
		print dir(result)

		# Go to link
		result.click()
		print dir(result)

		# Ensure result is in recent links
		recent = self.driver.find_elements_by_tag_name('li')[0]
		self.assertEqual(result.text, recent.text)

		
	
if __name__ == '__main__':
	unittest.main()

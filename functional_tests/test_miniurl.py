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
        self.assertIn('See what people are minifying!', self.driver.page_source)
        input = self.driver.find_element_by_name('url')
        test_url = 'http://selenium-python.readthedocs.org/'
        input.send_keys(test_url)
        input.send_keys(Keys.RETURN)

        # Shortened url appears below text input
        result = self.driver.find_element_by_id('result')

        # Go to link and ensure it is what we want.
        result.click()
        windows = self.driver.window_handles
        self.driver.switch_to_window(windows[1])
        self.assertEqual(test_url, self.driver.current_url)
        self.driver.close()
        self.driver.switch_to_window(windows[0])

        # Ensure result is in recent links
        recent = self.driver.find_elements_by_tag_name('li')[1]
        self.assertEqual(result.text, recent.text)


if __name__ == '__main__':
    unittest.main()

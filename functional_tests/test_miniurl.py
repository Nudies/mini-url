import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class BaseMiniUrl(unittest.TestCase):
    '''MiniUrl base testing class'''

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(5)
        self.driver.get('http://localhost:5000')

    def tearDown(self):
        self.driver.close()

    def submit_link(self, link):
        input = self.driver.find_element_by_name('url')
        input.send_keys(link)
        input.send_keys(Keys.RETURN)
        return self.driver.find_element_by_id('result')


class MiniUrl(BaseMiniUrl):

    def test_can_submit_link(self):
        # User sees a text input, puts in a url and
        # the shortened url appears below text input
        self.assertIn('Mini URL', self.driver.title)
        self.assertIn('See what people are minifying!', self.driver.page_source)
        test_url = 'http://selenium-python.readthedocs.org/'
        result = self.submit_link(test_url)

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

    def test_recent_urls_only_shows_ten(self):
        # User sees 'See what people are minifying!' and notices only 10 urls
        recent_links = self.driver.find_elements_by_tag_name('li')[1:]
        old_top = recent_links[0].text
        self.assertEqual(10, len(recent_links))

        # User submits a new link and sees there are still only 10 links,
        # but now his is on the top and the previous bottom is not.
        test_url = 'https://www.python.org/'
        result = self.submit_link(test_url)
        new_recent = self.driver.find_elements_by_tag_name('li')[1:]
        self.assertEqual(10, len(new_recent))
        self.assertNotEqual(old_top, new_recent[0].text)
        self.assertEqual(result.text, new_recent[0].text)


if __name__ == '__main__':
    unittest.main()

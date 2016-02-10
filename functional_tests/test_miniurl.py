from cases import BaseCase
from pages import MiniUrlPage


class MiniUrlCase(BaseCase):

    def setUp(self):
        BaseCase.setUp(self)
        self.page = MiniUrlPage(self.driver, navigate=True)

    def test_can_submit_and_follow_link(self):
        # Submit a new link
        result = self.page.submit_link()
        self.assertTrue(result.text)
        # Follow the results
        result.click()
        self.page.change_window(1)
        self.assertEqual(self.page.link, self.page.url)
        self.page.wd.close()
        self.page.change_window(0)
        # Ensure result is in recent links
        recent = self.page.new_recent_link()
        self.assertEqual(result.text, recent.text)

    def test_new_url_is_top_of_recent(self):
        # Everytime a new link is minified it should be at
        # the top of the recent list.
        for i in xrange(10):
            result = self.page.submit_link()
            recent = self.page.new_recent_link()
            self.assertEqual(result.text, recent.text)

    def test_max_ten_recent_links(self):
        for i in xrange(11):
            self.page.submit_link()
        recent_links = self.page.all_recent_links()
        self.assertEqual(10, len(recent_links))

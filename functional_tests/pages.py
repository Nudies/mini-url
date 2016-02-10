from config import SERVER


class PageObject(object):
    """
    Base page object
    """

    def __init__(self, wd):
        self.wd = wd
        self._title = None
        self._url = None

    @property
    def title(self):
        self._title = self.wd.title
        return self._title

    @property
    def url(self):
        self._url = self.wd.current_url
        return self._url

    def change_window(self, target=0):
        windows = self.wd.window_handles
        self.wd.switch_to_window(windows[target])


class MiniUrlPage(PageObject):
    """
    Interface to the main page
    """

    def __init__(self, wd, navigate=False, link=None):
        super(MiniUrlPage, self).__init__(wd)
        if link is None:
            # generic link to use for testing
            self.link = 'https://www.python.org/'
        else:
            self.link = link
        if navigate:
            self.wd.get(SERVER)

    def _set_input_field(self, text):
        field = self.wd.find_element_by_id('url')
        field.clear()
        field.send_keys(text)

    def _submit_form(self):
        btn = self.wd.find_element_by_css_selector('.input-group-btn .btn-success')
        btn.click()

    def _get_result(self):
        result = self.wd.find_element_by_id('result')
        return result

    def submit_link(self, link=None):
        self._set_input_field(link or self.link)
        self._submit_form()
        return self._get_result()

    def new_recent_link(self):
        return self.wd.find_elements_by_tag_name('li')[1]

    def all_recent_links(self):
        return self.wd.find_elements_by_tag_name('li')[1:]

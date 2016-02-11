import os
import json
import tempfile
import unittest
from datetime import datetime

import miniurl


class MiniUrlBaseCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.path = tempfile.mkstemp()
        miniurl.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.path
        miniurl.app.config['TESTING'] = True
        self.db = miniurl.db
        self.db.create_all()
        self.app = miniurl.app.test_client()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()
        os.close(self.db_fd)
        os.unlink(self.path)


class MiniUrlRoutesTestCase(MiniUrlBaseCase):

    def test_can_get_homepage(self):
        res = self.app.get('/')
        self.assertEqual(200, res.status_code)
        self.assertIn('Mini URL', res.data)

    def test_can_post_homepage(self):
        res = self.app.post(
            '/',
            data=dict(url='http://foobar.com'),
            follow_redirects=True
        )
        self.assertEqual(200, res.status_code)
        self.assertIn('Mini URL', res.data)

    def test_can_get_statspage(self):
        res = self.app.get('/stats')
        self.assertEqual(200, res.status_code)


class MiniUrlStatTestCase(MiniUrlBaseCase):

    def setUp(self):
        MiniUrlBaseCase.setUp(self)
        stats = miniurl.Stats(
            'foo platform',
            'foo browser',
            'foo version',
            'foo language',
            'foo ua string',
            'foo ip'
        )
        self.db.session.add(stats)
        self.db.session.commit()

    def get_endpoint(self, endpoint):
        res = self.app.get('/data/' + endpoint)
        data = json.loads(res.data)
        return res, data

    def test_can_get_data_browsers_endpoint(self):
        res, data = self.get_endpoint('browsers')
        self.assertEqual('application/json', res.mimetype)
        self.assertIn('foo browser', data.keys())

    def test_can_get_data_platforms_endpoint(self):
        res, data = self.get_endpoint('platforms')
        self.assertEqual('application/json', res.mimetype)
        self.assertIn('foo platform', data.keys())

    def test_can_get_data_months_endpoint(self):
        res, data = self.get_endpoint('months')
        month_today = datetime.today().strftime('%b')
        self.assertEqual('application/json', res.mimetype)
        self.assertIn(month_today, data.keys())

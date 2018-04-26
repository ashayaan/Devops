import os
import flask
import urllib2
import unittest
import tempfile
from server import app, mysql
from flask_testing import LiveServerTestCase

class FlaskTestCase(unittest.TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def login(self, username, password):
        return self.app.post('http://0.0.0.0:5000/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('http://0.0.0.0:5000/logout', follow_redirects=True)

    def register(self, name, email, username, password):
        return self.app.post(
        'http://0.0.0.0:5000/signUp',
        data=dict(name = name, email=email, username=username, password=password),
        follow_redirects=True
    )


    def setUp(self):
        # self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        # flaskr.app.testing = True
        # self.app = flaskr.app.test_client()
        # with flaskr.app.app_context():
        #     flaskr.init_db()
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        # os.close(self.db_fd)
        # os.unlink(flaskr.app.config['DATABASE'])
        pass

    def test_1_home_status_code(self):
        result = self.app.get('/signin')
        self.assertEqual(result.status_code, 200) 

    # def test_flask_application_is_up_and_running(self):
    #     response = urllib2.urlopen("http://0.0.0.0:5000/")
    #     self.assertEqual(response.code, 200)     

    # def test_registration(self):

    def test_2_valid_user_registration(self):
        response = self.register('PatKen', 'patkennedy79@gmail.com', 'patkennedy79', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)
        # print response.data
        self.assertNotIn(b'Username already existts', response.data)
        self.assertNotIn(b'Enter all the details', response.data)
        # self.assertTrue(response.data)

    def test_3_invalid_user_registration(self):
        response = self.register('PatKen', 'patkennedy79@gmail.com', 'patkennedy79', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)
        # print response.data
        self.assertIn(b'Username already existts', response.data)
        # self.assertTrue(response.data)


    def test_4_valid_login_logout(self):
        response = self.login('patkennedy79', 'FlaskIsAwesome')
        # print response.data
        # print help(self.app)
        # assert 'You were logged in' in response.data
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Username or Password Wrong!', response.data)
        rv = self.logout()
        # assert 'You were logged out' in rv.data
        self.assertEqual(rv.status_code, 200)
        # rv = self.login('adminx', 'default')
        # assert 'Invalid username' in rv.data
        # rv = self.login('admin', 'defaultx')
        # assert 'Invalid password' in rv.data
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute('delete from users where username="patkennedy79"')
        conn.commit()
        

if __name__ == '__main__':
    unittest.main()
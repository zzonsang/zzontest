"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client

class ViewTest(TestCase):
    fixtures = ['test_data.json']
    def setUp(self):
        self.client = Client()
        
    def test_register_page(self):
        data = {
                'username' : 'tester',
                'email' : 'tester@example.com',
                'password1' : '123',
                'password2' : '123',
                }
        response = self.client.post('/register/', data)
        self.assertEqual(response.status_code, 302)

    def test_bookmark_save(self):
#        self.client.login('/save/', {'username':'test_user', 'password':'pass123'})
        response = self.client.login(username='kobe', password='123')
        self.assertTrue(response)

        data = { 
                'url' : 'http://www.naver.com/',
                'title' : 'Test URL',
                'tags' : 'test-tag'
                }
        response = self.client.post('/save/', data)
        self.assertEqual(response.status_code, 302)
        
        response = self.client.get('/user/kobe/')
        self.assertTrue('http://www.naver.com/' in response.content)
        self.assertTrue('Test URL' in response.content)
        self.assertTrue('test-tag' in response.content)
        
        
from flask import Flask
from flask_testing import TestCase
import run as myApp

class TestFlaskBase(TestCase):
    def create_app(self):
        self.app = myApp.app
        return myApp.app

        self.app = app
        return app
    
    def setUp(self):
        self.client = self.app.test_client()
        self.client.testing = True

    def tearDown(self):
        pass
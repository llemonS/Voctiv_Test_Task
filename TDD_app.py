from app import *
from distance_finder.api import *
from distance_finder.mkad import *
from os import environ
import unittest
import json

app.testing = True

class APITests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_get_home(self):
        #verify if the route exists
        response = self.app.get("/")
        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.headers['Content-Type'])

    def test_wrong_route(self):
        response = self.app.get("/test")
        self.assertEqual(404, response.status_code)
        self.assertEqual("application/json", response.headers['Content-Type'])
        self.assertEqual({"message":"This endpoint does not exists."}, response.get_json())

    def test_route_with_wrong_method(self):
        response = self.app.delete("/")
        self.assertEqual(405, response.status_code)
        self.assertEqual("application/json", response.headers['Content-Type'])
        self.assertEqual({"message":"Sorry, this method is not allowed in our API."}, response.get_json())

    def test_post_address_inside_mkad(self):
        response = self.app.post("/", data=json.dumps({"address":"Moscow Planetarium, Moscow, Russia"}), headers={'Content-Type': 'application/json'})
        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.headers['Content-Type'])
        self.assertEqual({"message": "This address is located inside MKAD."}, response.get_json())

    def test_post_address_outside_mkad(self):
        response = self.app.post("/", data=json.dumps({"address":"Eiffel Tower, Paris, France"}), headers={'Content-Type': 'application/json'})
        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.headers['Content-Type'])
        self.assertEqual({"message": "This address is 1566.43 km far from the centroid of MKAD polygon points with confidence 0.8"}, response.get_json())

if __name__ == "__main__":
    
    unittest.main()
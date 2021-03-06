import unittest
import json
from app import create_app, db

class BusinessTestCase(unittest.TestCase):
    """Test case for the business endpoint """
    def setUp(self):
        #create app using the flask import
        self.app = create_app('testing')

        #create a test client
        self.client = self.app.test_client

        #create a dict to be used to add a new biz
        self.a_business = {'name':'Xedrox',
                            'category': 'IT',
                            'location' : 'Lira'
                            }
        
        #create a dict to be used to edit business
        self.edited_business = {'name':'Megatrends',
                                'category': 'Confectionary',
                                'location' : 'Kampala'
                            }

        #create a dict to be used to store the review
        self.a_business_review = {'review_summary':'Good stuff',
                                'review_description': 'I liked every thing about it',
                                'star_rating' : '5'
                            }
                            
        #create a dict to be used to store user details
        self.user_data = {
            'username': 'roger',
            'password': 'okello'
        }

        #bind the app context
        with self.app.app_context():
            pass

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # delete database contents
            db.businesses.clear()
            db.reviews.clear()
            db.users.clear()

    def register_user(self, username="roger", password="okello"):
        """This helper method helps register a test user."""
        user_data = {
            'username': username,
            'password': password
        }
        return self.client().post('/auth/register',
                                 data=json.dumps(self.user_data),
                                 content_type='application/json'
                                 )
    
    def login_user(self, username="roger", password="okello"):
        """This helper method helps log in a test user."""
        user_data = {
            'username': username,
            'password': password
        }
        return self.client().post('/auth/login',
                                        data=json.dumps(self.user_data),
                                        content_type='application/json'
                                )

    # helper method to get access token
    def get_token(self):
        #register user first
        self.register_user()

        #login user
        result = self.login_user()

        # obtain the access token from result
        access_token = json.loads(result.data.decode())['access_token']
        
        return access_token

    def test_new_business_can_be_added(self):
        """Test the API can create a business (POST request)"""
        
        response = self.client().post('/businesses',
                                headers=dict(Authorization="Bearer " + self.get_token()),
                                data=json.dumps(self.a_business),
                                content_type='application/json')

        #check that a 201 response status code was returned
        self.assertEqual(response.status_code, 201)

        # check that Created business string in returned json response
        self.assertIn('Created business: ', str(response.data))

    def test_api_can_get_all_businesses(self):
        """Test the API can get all business registered businesses (GET request)"""
        # register a test user, then log them in
        self.register_user()
        result = self.login_user()

        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']

        # first add a business
        self.client().post('/businesses', 
                                headers=dict(Authorization="Bearer " + access_token),
                                data=json.dumps(self.a_business),
                                content_type='application/json')

        response = self.client().get('/businesses',
                                    headers=dict(Authorization="Bearer " + access_token)
                                    )

        #check that a 201 response status code was returned
        self.assertEqual(response.status_code, 201)

        # check that Xedrox string in returned json response
        self.assertIn('Xedrox', str(response.data))

    def test_api_can_get_business_by_id(self):
        """Test the API can get a business by ID (GET request)"""
        # register a test user, then log them in
        self.register_user()
        result = self.login_user()

        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']

        # first add a business
        self.client().post('/businesses',
                                headers=dict(Authorization="Bearer " + access_token),
                                data=json.dumps(self.a_business),
                                content_type='application/json')

        response = self.client().get('/businesses/0',
                                    headers=dict(Authorization="Bearer " + access_token)
                                )

        #check that a 201 response status code was returned
        self.assertEqual(response.status_code, 201)

        # check that Xedrox string in returned json response
        self.assertIn('Xedrox', str(response.data))

    def test_api_can_remove_a_business_by_id(self):
        """Test the API can remove a business given an id (DELETE request)"""
        # register a test user, then log them in
        self.register_user()
        result = self.login_user()

        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']

        # first add a business
        self.client().post('/businesses',
                                headers=dict(Authorization="Bearer " + access_token),
                                data=json.dumps(self.a_business),
                                content_type='application/json')
        
        #delete the business by its id
        response = self.client().delete('/businesses/0',
                                        headers=dict(Authorization="Bearer " + access_token)
                                        )

        #check that a 201 response status code was returned
        self.assertEqual(response.status_code, 201)

        # check that Business deleted string in returned json response
        self.assertIn('Business deleted', str(response.data))

    def test_api_can_modify_a_business_profile(self):
        """Test the API can modify a business profile (PUT request)"""
        # register a test user, then log them in
        self.register_user()
        result = self.login_user()

        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']

        # first add a business
        self.client().post('/businesses',
                            headers=dict(Authorization="Bearer " + access_token),
                            data=json.dumps(self.a_business),
                            content_type='application/json')

        # Edit business 
        response = self.client().put('/businesses/0',
                            headers=dict(Authorization="Bearer " + access_token),
                            data=json.dumps(self.edited_business),
                            content_type='application/json')

        #check that a 201 response status code was returned
        self.assertEqual(response.status_code, 201)

        # check that Megatrends string in returned json response
        self.assertIn('Megatrends', str(response.data))

    def test_api_can_create_a_business_review(self):
        """Test the API can create a business review (POST request)"""
        # register a test user, then log them in
        self.register_user()
        result = self.login_user()

        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']

        #first create a business
        self.client().post('/businesses',
                            headers=dict(Authorization="Bearer " + access_token),
                            data=json.dumps(self.a_business),
                            content_type='application/json')

        #make the review
        response = self.client().post('/businesses/0/reviews',
                            headers=dict(Authorization="Bearer " + access_token),
                            data=json.dumps(self.a_business_review),
                            content_type='application/json')

        #check that a 201 response status code was returned
        self.assertEqual(response.status_code, 201)

        # check that Good stuff string in returned json response
        self.assertIn('Good stuff', str(response.data))


    def test_api_can_get_all_business_review(self):
        """Test the API can get all business reviews (GET request)"""
        # register a test user, then log them in
        self.register_user()
        result = self.login_user()

        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']

        #first create a business
        self.client().post('/businesses',
                            headers=dict(Authorization="Bearer " + access_token),
                            data=json.dumps(self.a_business),
                            content_type='application/json')

        #make the review
        self.client().post('/businesses/0/reviews',
                            headers=dict(Authorization="Bearer " + access_token),
                            data=json.dumps(self.a_business_review),
                            content_type='application/json')

        #get all the reviews
        response = self.client().get('/businesses/0/reviews',
                                    headers=dict(Authorization="Bearer " + access_token)
                                    )

        # check that Good stuff string in returned json response
        self.assertIn('Good stuff', str(response.data))

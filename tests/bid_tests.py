import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from quickbidsapi.models import Contractor, Bid, Job
from rest_framework.authtoken.models import Token


class BidTests(APITestCase):

    fixtures = ['users', 'tokens', 'contractors',
                'jobs', 'fields', 'job_fields', 'bids']

    def setUp(self):
        # Seed the database with a user (use a unique username)
        user_1 = User.objects.create(username="gatoradephilips", password="password", first_name="Gatorade", last_name="Philips",
                                     email="gatorade@philips.com", is_staff=False, is_active=True, date_joined="2022-10-21T21:19:24.892Z")

        # Seed the database with a contractor
        self.sub = Contractor.objects.create(
            user=user_1, company_name="Philips Gatorade", phone_number="555-3579", primary_contractor=False)

        # Seed the database with a user (use a unique username)
        user_2 = User.objects.create(username="danielmyers", password="password", first_name="Daniel", last_name="Myers",
                                     email="daniel@library.com", is_staff=False, is_active=True, date_joined="2022-10-21T21:19:24.892Z")

        # Seed the database with a contractor
        self.primary = Contractor.objects.create(
            user=user_2, company_name="Daniel Co", phone_number="555-6543", primary_contractor=True)
        # Create a Token for the user if it doesn't exist

        token, created = Token.objects.get_or_create(user=self.sub.user)
        # Set the client's credentials using the Token
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_bid(self):
        """
        Ensure we can create a new bid.
        """
        # Define the endpoint in the API to which
        # the request will be sent
        url = "/bids"

        # Define the request body
        data = {
            "rate": 17,
            "job": 1,
            "primary": self.primary.id,
            "sub": self.sub.id,
            "is_request": False
        }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["rate"], 17)
        self.assertEqual(json_response["job"], {
            "id": 1,
            "name": "EyeMasters"
        })
        self.assertEqual(
            json_response["primary_contractor"], {'id': 8, 'company_name': 'Daniel Co'})
        self.assertEqual(
            json_response["sub_contractor"], {'id': 7, 'company_name': 'Philips Gatorade'})
        self.assertEqual(json_response["accepted"], False)
        self.assertEqual(json_response["is_request"], False)

    def test_get_bid(self):
        """
        Ensure we can get an existing bid
        """

        url = "/bids"

        # Define the request body
        data = {
            "rate": 17,
            "job": 1,
            "primary": self.primary.id,
            "sub": self.sub.id,
            "is_request": False
        }

        # Initiate request and store response
        self.client.post(url, data, format='json')
        bid = Bid.objects.last()

        # Initiate request and store response
        response = self.client.get(f"/bids/{bid.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the bid was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["rate"], 17)
        self.assertEqual(json_response["job"], {
            "id": 1,
            "name": "EyeMasters"
        })
        self.assertEqual(
            json_response["primary_contractor"], {'id': 8, 'company_name': 'Daniel Co'})
        self.assertEqual(
            json_response["sub_contractor"], {'id': 7, 'company_name': 'Philips Gatorade'})
        self.assertEqual(json_response["accepted"], False)
        self.assertEqual(json_response["is_request"], False)

    def test_change_bid(self):
        """
        Ensure we can change an existing bid.
        """

        url = "/bids"

        # Define the request body
        data = {
            "rate": 17,
            "job": 1,
            "primary": self.primary.id,
            "sub": self.sub.id,
            "is_request": False
        }

        # Initiate request and store response
        self.client.post(url, data, format='json')
        bid = Bid.objects.last()

        # DEFINE NEW PROPERTIES FOR BID
        data = {
            "rate": 19,
            "job": 3,
            "primary": 2,
            "sub": 4,
            "accepted": True,
            "is_request": False
        }

        response = self.client.put(
            f"/bids/{bid.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET bid again to verify changes were made
        response = self.client.get(f"/bids/{bid.id}")
        json_response = json.loads(response.content)

        # Assert that the properties are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["rate"], 19)
        self.assertEqual(json_response["job"], {
                         'id': 3, 'name': 'OptiNova Solutions'})
        self.assertEqual(json_response["primary_contractor"], {
                         'id': 2, 'company_name': 'Ducharme Construction'})
        self.assertEqual(json_response["sub_contractor"], {
                         'id': 4, 'company_name': 'Nilson Painting'})
        self.assertEqual(json_response["accepted"], True)
        self.assertEqual(json_response["is_request"], False)

    def test_delete_bid(self):
        """
        Ensure we can delete an existing bid.
        """

        url = "/bids"

        # Define the request body
        data = {
            "rate": 17,
            "job": 1,
            "primary": self.primary.id,
            "sub": self.sub.id,
            "is_request": False
        }

        # Initiate request and store response
        self.client.post(url, data, format='json')
        bid = Bid.objects.last()

        # DELETE the bid you just created
        response = self.client.delete(f"/bids/{bid.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the bid again to verify you get a 404 response
        response = self.client.get(f"/bids/{bid.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

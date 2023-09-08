import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from quickbidsapi.models import Contractor, Bid, Job
from rest_framework.authtoken.models import Token


class BidTests(APITestCase):

    fixture = ['users', 'tokens', 'contractors',
               'jobs', 'fields', 'job_fields', 'bids']

    def setUp(self):
        # Try to retrieve the first existing Contractor object
        self.contractor = Contractor.objects.first()

        if self.contractor is None:
            # If no Contractor exists, create one
            self.user = User.objects.create(username="testuser")
            self.contractor = Contractor.objects.create(
                user=self.user, company_name="Test Company")

        # Create a Token for the user if it doesn't exist
        token, created = Token.objects.get_or_create(user=self.contractor.user)

        # Set the client's credentials using the Token
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_bid(self):
        """
        Ensure we can create a new bid.
        """
        # Define the endpoint in the API to which
        # the request will be sent
        url = "/bids"

        # Seed the database with a job
        job = Job.objects.create(name="OptiNova Solutions")

        # Define the request body
        data = {
            "rate": 17,
            "job": 1,
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
            json_response["contractor"], Contractor.objects.last())
        self.assertEqual(json_response["accepted"], False)

    def test_get_bid(self):
        """
        Ensure we can get an existing bid
        """

        # Seed the database with a bid
        bid = Bid.objects.create(rate=17, job=1)

        # Initiate request and store response
        response = self.client.get(f"/bids/{bid.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the bid was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["rate"], 17)
        self.assertEqual(json_response["job"], 1)
        self.assertEqual(
            json_response["contractor"], Contractor.objects.last())
        self.assertEqual(json_response["accepted"], False)

    def test_change_bid(self):
        """
        Ensure we can change an existing bid.
        """

        # Seed the database with a bid
        bid = Bid.objects.create(rate=17, job=1)

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "rate": 19,
            "job": {3, "OptiNova Solutions"},
            "contractor": {4, "Nilson Painting"},
            "accepted": True
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
        self.assertEqual(json_response["job"], {3, "OptiNova Solutions"})
        self.assertEqual(json_response["contractor"], {4, "Nilson Painting"})
        self.assertEqual(json_response["accepted"], True)

    def test_delete_bid(self):
        """
        Ensure we can delete an existing bid.
        """

        # Seed the database with a bid
        bid = Bid.objects.create(rate=17, job=1)

        # DELETE the bid you just created
        response = self.client.delete(f"/bids/{bid.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the bid again to verify you get a 404 response
        response = self.client.get(f"/bids/{bid.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
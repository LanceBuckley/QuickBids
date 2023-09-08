import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from quickbidsapi.models import Contractor, Job, Field
from rest_framework.authtoken.models import Token


class JobTests(APITestCase):

    fixtures = ['users', 'tokens', 'contractors',
               'jobs', 'fields', 'job_fields', 'bids']

    def setUp(self):

        # Try to retrieve the first existing Contractor object
        self.contractor = Contractor.objects.first()

        # Create a Token for the user if it doesn't exist
        token, created = Token.objects.get_or_create(user=self.contractor.user)

        # Set the client's credentials using the Token
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_job(self):
        """
        Ensure we can create a new job.
        """
        # Define the endpoint in the API to which
        # the request will be sent
        url = "/jobs"

        # Define the request body
        data = {
            "fields": [1, 2, 3],
            "name": "Test Job",
            "address": "123 Testing Rd.",
            "blueprint": "",
            "square_footage": 1700
        }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(
            json_response["contractor"], {"id": 1, "company_name": "Tanay Building Group"})
        self.assertEqual(json_response["name"], "Test Job")
        self.assertEqual(json_response["address"], "123 Testing Rd.")
        self.assertEqual(
            json_response["fields"],
            [{"id": 1, "job_title": "Painting"}, {"id": 2, "job_title": "Drywall"},
                {"id": 3, "job_title": "Epoxy Flooring"}]
        )
        self.assertEqual(json_response["blueprint"], None)
        self.assertEqual(json_response["square_footage"], 1700)
        self.assertEqual(json_response["open"], True)
        self.assertEqual(json_response["complete"], False)

    def test_get_job(self):
        """
        Ensure we can get an existing job
        """

        # Seed the database with a job
        job = Job.objects.create(rate=17, job=1)

        # Initiate request and store response
        response = self.client.get(f"/jobs/{job.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the job was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["rate"], 17)
        self.assertEqual(json_response["job"], 1)
        self.assertEqual(
            json_response["contractor"], Contractor.objects.last())
        self.assertEqual(json_response["accepted"], False)

    def test_change_job(self):
        """
        Ensure we can change an existing job.
        """

        # Seed the database with a job
        job = Job.objects.create(rate=17, job=1)

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "rate": 19,
            "job": {3, "OptiNova Solutions"},
            "contractor": {4, "Nilson Painting"},
            "accepted": True
        }

        response = self.client.put(
            f"/jobs/{job.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET job again to verify changes were made
        response = self.client.get(f"/jobs/{job.id}")
        json_response = json.loads(response.content)

        # Assert that the properties are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["rate"], 19)
        self.assertEqual(json_response["job"], {3, "OptiNova Solutions"})
        self.assertEqual(json_response["contractor"], {4, "Nilson Painting"})
        self.assertEqual(json_response["accepted"], True)

    def test_delete_job(self):
        """
        Ensure we can delete an existing job.
        """

        # Seed the database with a job
        job = Job.objects.create(rate=17, job=1)

        # DELETE the job you just created
        response = self.client.delete(f"/jobs/{job.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the job again to verify you get a 404 response
        response = self.client.get(f"/jobs/{job.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

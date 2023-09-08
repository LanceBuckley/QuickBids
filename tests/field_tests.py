import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from quickbidsapi.models import Contractor, Field
from rest_framework.authtoken.models import Token


class FieldTests(APITestCase):

    fixture = ['users', 'tokens', 'fields',
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

    def test_create_field(self):
        """
        Ensure we can create a new field.
        """
        # Define the endpoint in the API to which
        # the request will be sent
        url = "/fields"

        # Define the request body
        data = {
            "job_title": "Complainer",
        }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["job_title"], "Complainer")

    def test_get_field(self):
        """
        Ensure we can get an existing field
        """

        # Seed the database with a field
        field = Field.objects.create(job_title="Complainer")

        # Initiate request and store response
        response = self.client.get(f"/fields/{field.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the field was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["job_title"], "Complainer")

    def test_change_field(self):
        """
        Ensure we can change an existing field.
        """

        # Seed the database with a field
        field = Field.objects.create(job_title="Complainer")

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "job_title": "Manager",
        }

        response = self.client.put(
            f"/fields/{field.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET field again to verify changes were made
        response = self.client.get(f"/fields/{field.id}")
        json_response = json.loads(response.content)

        # Assert that the properties are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["job_title"], "Manager")

    def test_delete_field(self):
        """
        Ensure we can delete an existing field.
        """

        # Seed the database with a field
        field = Field.objects.create(job_title="Complainer")

        # DELETE the field you just created
        response = self.client.delete(f"/fields/{field.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the field again to verify you get a 404 response
        response = self.client.get(f"/fields/{field.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

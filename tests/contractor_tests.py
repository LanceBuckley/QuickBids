import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from quickbidsapi.models import Contractor, Job, Field, JobField, Bid
from rest_framework.authtoken.models import Token


class ContractorTests(APITestCase):

    fixtures = ['users', 'tokens', 'contractors',
               'jobs', 'fields', 'job_fields', 'bids']

    def setUp(self):
        # Try to retrieve the first existing Contractor object
        self.contractor = Contractor.objects.first()
        # Create a Token for the user if it doesn't exist
        token, created = Token.objects.get_or_create(user=self.contractor.user)
        # Set the client's credentials using the Token
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_get_contractor(self):
        """
        Ensure we can get an existing contractor
        """

        # Seed the database with a user (use a unique username)
        user = User.objects.create(username="gatoradephilips", password="password", first_name="Gatorade", last_name="Philips",
                                   email="gatorade@philips.com", is_staff=False, is_active=True, date_joined="2022-10-21T21:19:24.892Z")

        # Seed the database with a contractor
        contractor = Contractor.objects.create(
            user=user, company_name="Philips Gatorade", phone_number="555-3579", primary_contractor=True)

        # Initiate request and store response
        response = self.client.get(f"/contractors/{contractor.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the contractor was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["company_name"], "Philips Gatorade")
        self.assertEqual(json_response["phone_number"], "555-3579")
        self.assertEqual(json_response["primary_contractor"], True)

    def test_change_contractor(self):
        """
        Ensure we can change an existing contractor.
        """
        # Seed the database with a user (use a unique username)
        user = User.objects.create(username="gatoradephilips", password="password", first_name="Gatorade", last_name="Philips",
                                   email="gatorade@philips.com", is_staff=False, is_active=True, date_joined="2022-10-21T21:19:24.892Z")

        # Seed the database with a contractor
        contractor = Contractor.objects.create(
            user=user, company_name="Philips Gatorade", phone_number="555-3579", primary_contractor=True)

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "first_name": "Daniel",
            "last_name": "Myers",
            "username": "danielmyers",
            "email": "daniel@myers.com",
            "company_name": "Myers Building Group",
            "phone_number": "555-0987",
            "primary_contractor": False
        }

        response = self.client.put(
            f"/contractors/{contractor.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET contractor again to verify changes were made
        response = self.client.get(f"/contractors/{contractor.id}")
        json_response = json.loads(response.content)

        # Assert that the properties are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["first_name"], "Daniel")
        self.assertEqual(json_response["last_name"], "Myers")
        self.assertEqual(json_response["username"], "danielmyers")
        self.assertEqual(json_response["email"], "daniel@myers.com")
        self.assertEqual(json_response["company_name"], "Myers Building Group")
        self.assertEqual(json_response["phone_number"], "555-0987")
        self.assertEqual(json_response["primary_contractor"], False)

    def test_delete_contractor(self):
        """
        Ensure we can delete an existing contractor.
        """
        # Seed the database with a user (use a unique username)
        user = User.objects.create(username="gatoradephilips", password="password", first_name="Gatorade", last_name="Philips",
                                   email="gatorade@philips.com", is_staff=False, is_active=True, date_joined="2022-10-21T21:19:24.892Z")

        # Seed the database with a contractor
        contractor = Contractor.objects.create(
            user=user, company_name="Philips Gatorade", phone_number="555-3579", primary_contractor=True)

        # DELETE the contractor you just created
        response = self.client.delete(f"/contractors/{contractor.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the contractor again to verify you get a 404 response
        response = self.client.get(f"/contractors/{contractor.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

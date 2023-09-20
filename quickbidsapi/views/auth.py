from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from quickbidsapi.models import Contractor


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    '''Handles the authentication of a user

    Method arguments:
      request -- The full HTTP request object
    '''
    username = request.data['username']
    password = request.data['password']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    authenticated_user = authenticate(username=username, password=password)

    # If authentication was successful, respond with their token
    if authenticated_user is not None and authenticated_user.is_active:
        token = Token.objects.get(user=authenticated_user)
        contractor = Contractor.objects.get(user=authenticated_user)

        data = {
            'valid': True,
            'token': token.key,
            'staff': authenticated_user.is_staff,
            'primary': contractor.primary_contractor
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = {'valid': False}
        return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''
    account_type = 'contractor'
    email = request.data.get('email', None)
    first_name = request.data.get('first_name', None)
    last_name = request.data.get('last_name', None)
    username = request.data.get('username', None)
    password = request.data.get('password', None)
    company_name = request.data.get('company_name', None)
    phone_number = request.data.get('phone_number', None)
    primary_contractor = request.data.get('primary_contractor', None)

    if account_type is not None \
            and email is not None\
            and first_name is not None \
            and last_name is not None \
            and username is not None \
            and password is not None \
            and company_name is not None \
            and phone_number is not None \
            and primary_contractor is not None :

        try:
            # Create a new user by invoking the `create_user` helper method
            # on Django's built-in User model
            new_user = User.objects.create_user(
                username=request.data['username'],
                email=request.data['email'],
                password=request.data['password'],
                first_name=request.data['first_name'],
                last_name=request.data['last_name']
            )
        except IntegrityError:
            return Response(
                {'message': 'An account with that email address already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        account = None

        if account_type == 'contractor':
            account = Contractor.objects.create(
                user=new_user,
                company_name=request.data['company_name'],
                phone_number=request.data['phone_number'],
                primary_contractor=request.data['primary_contractor']
            )

        # Use the REST Framework's token generator on the new user account
        token = Token.objects.create(user=account.user)
        # Return the token to the client
        data = {'token': token.key, 'staff': new_user.is_staff, 'primary': account.primary_contractor, 'valid': True}
        return Response(data)

    return Response({'message': 'You must provide email, password, first_name, last_name, and username'}, status=status.HTTP_400_BAD_REQUEST)

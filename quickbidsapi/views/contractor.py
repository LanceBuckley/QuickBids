from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from quickbidsapi.models import Contractor


class ContractorView(ViewSet):

    def list(self, request):
        """
        Summary:
            Retrieve a list of contractors based on query parameters.

        Args:
            request (HttpRequest): The full HTTP request object.

        Returns:
            Response: A serialized dictionary and HTTP status 200 OK.
        """
        contractors = Contractor.objects.all()

        if request.query_params.get('primary_contractor') is not None:
            if request.query_params.get('primary_contractor') == 'true':
                contractors = contractors.filter(primary_contractor=True)
            elif request.query_params.get('primary_contractor') == 'false':
                contractors = contractors.filter(primary_contractor=False)

        if "current" in request.query_params:
            contractors = contractors.filter(user=request.auth.user)

        serializer = ContractorSerializer(contractors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        Summary:
            Retrieve a specific contractor by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the contractor to retrieve.

        Returns:
            Response: A serialized dictionary containing the contractor's data and HTTP status 200 OK,
            or HTTP status 404 Not Found if the contractor with the specified primary key does not exist.
        """
        try:
            contractor = Contractor.objects.get(pk=pk)
            serializer = ContractorSerializer(contractor, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Contractor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """
        Summary:
            Update a specific contractor's user information by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the contractor to update.

        Returns:
            Response: A successful HTTP status 204 No Content response after updating the contractor's user details,
            or HTTP status 404 Not Found if the contractor with the specified primary key does not exist.
        """
        try:
            contractor = Contractor.objects.get(pk=pk)
            contractor.user.first_name = request.data["first_name"]
            contractor.user.last_name = request.data["last_name"]
            contractor.user.username = request.data["username"]
            contractor.user.email = request.data["email"]
            contractor.user.save()
            contractor.company_name = request.data["company_name"]
            contractor.phone_number = request.data["phone_number"]
            contractor.primary_contractor = request.data["primary_contractor"]
            contractor.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Contractor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """
        Summary:
            Delete a specific contractor and associated user by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the contractor to delete.

        Returns:
            Response: A successful HTTP status 204 No Content response after deletion,
            or HTTP status 404 Not Found if the contractor with the specified primary key does not exist.
        """

        try:
            contractor = Contractor.objects.get(pk=pk)
            user = contractor.user
            contractor.delete()
            user.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Contractor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ContractorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contractor
        fields = ('id', 'first_name', 'last_name', 'username', 'email',
                  'company_name', 'phone_number', 'primary_contractor', 'full_name')

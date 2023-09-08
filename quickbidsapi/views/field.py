from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from quickbidsapi.models import Field


class FieldView(ViewSet):

    def list(self, request):
        """
        Summary:
            Retrieve a list of fields based on query parameters.

        Args:
            request (HttpRequest): The full HTTP request object.

        Returns:
            Response: A serialized dictionary and HTTP status 200 OK.
        """
        fields = Field.objects.all()

        serializer = FieldSerializer(fields, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        Summary:
            Retrieve a specific field by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the field to retrieve.

        Returns:
            Response: A serialized dictionary containing the field's data and HTTP status 200 OK,
            or HTTP status 404 Not Found if the field with the specified primary key does not exist.
        """
        try:
            field = Field.objects.get(pk=pk)
            serializer = FieldSerializer(field, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Field.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """
        Summary:
            Update a specific field's user information by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the field to update.

        Returns:
            Response: A successful HTTP status 204 No Content response after updating the field's user details,
            or HTTP status 404 Not Found if the field with the specified primary key does not exist.
        """
        try:
            field = Field.objects.get(pk=pk)
            field.job_title = request.data["job_title"]
            field.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Field.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """
        Summary:
            Delete a specific field and associated user by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the field to delete.

        Returns:
            Response: A successful HTTP status 204 No Content response after deletion,
            or HTTP status 404 Not Found if the field with the specified primary key does not exist.
        """

        try:
            field = Field.objects.get(pk=pk)
            field.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Field.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class FieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = Field
        fields = ('id', 'job_title',)

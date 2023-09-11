from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from quickbidsapi.models import Job, Contractor, Field


class JobView(ViewSet):

    def list(self, request):
        """
        Summary:
            Retrieve a list of jobs based on query parameters.

        Args:
            request (HttpRequest): The full HTTP request object.

        Returns:
            Response: A serialized dictionary and HTTP status 200 OK.
        """
        jobs = Job.objects.all()

        if "contractor" in request.query_params:
            jobs = jobs.filter(contractor=request.query_params.get('contractor'))
        if request.query_params.get('open') is not None:
            if request.query_params.get('open') == 'true':
                jobs = jobs.filter(open=True)
            elif request.query_params.get('open') == 'false':
                jobs = jobs.filter(open=False)

        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        Summary:
            Retrieve a specific job by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the job to retrieve.

        Returns:
            Response: A serialized dictionary containing the job's data and HTTP status 200 OK,
            or HTTP status 404 Not Found if the job with the specified primary key does not exist.
        """
        try:
            job = Job.objects.get(pk=pk)
            serializer = JobSerializer(job, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Job.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """
        Summary:
            Create a new object using the request data

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the job to retrieve.

        Returns:
            Response: A serialized dictionary containing the job's data and HTTP status 201 Created.
        """
        contractor = Contractor.objects.get(user=request.auth.user)
        fields = Field.objects.filter(pk__in=request.data["fields"])

        job = Job.objects.create(
            contractor=contractor,
            name=request.data["name"],
            address=request.data["address"],
            blueprint=request.data["blueprint"],
            square_footage=request.data["square_footage"],
            open=True,
            complete=False,
        )

        job.fields.set(fields)

        serializer = JobSerializer(job, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """
        Summary:
            Update a specific job's user information by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the job to update.

        Returns:
            Response: A successful HTTP status 204 No Content response after updating the job's user details,
            or HTTP status 404 Not Found if the job with the specified primary key does not exist.
        """
        try:
            job = Job.objects.get(pk=pk)
            fields = Field.objects.filter(pk__in=request.data["fields"])
            job.contractor = Contractor.objects.get(
                pk=request.data["contractor"])
            job.name = request.data["name"]
            job.address = request.data["address"]
            job.blueprint = request.data["blueprint"]
            job.square_footage = request.data["square_footage"]
            job.open = request.data["open"]
            job.complete = request.data["complete"]
            job.fields.set(fields)
            job.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Job.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """
        Summary:
            Delete a specific job and associated user by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the job to delete.

        Returns:
            Response: A successful HTTP status 204 No Content response after deletion,
            or HTTP status 404 Not Found if the job with the specified primary key does not exist.
        """

        try:
            job = Job.objects.get(pk=pk)
            job.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Job.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ('id', 'job_title',)


class ContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contractor
        fields = ('id', 'company_name',)


class JobSerializer(serializers.ModelSerializer):

    fields = FieldSerializer(many=True)
    contractor = ContractorSerializer(many=False)

    class Meta:
        model = Job
        fields = ('id', 'contractor', 'fields', 'name', 'address',
                  'blueprint', 'square_footage', 'open', 'complete',)

from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from quickbidsapi.models import Bid, Job, Contractor


class BidView(ViewSet):

    def list(self, request):
        """
        Summary:
            Retrieve a list of bids based on query parameters.

        Args:
            request (HttpRequest): The full HTTP request object.

        Returns:
            Response: A serialized dictionary and HTTP status 200 OK.
        """
        bids = Bid.objects.all()

        if "sub" in request.query_params:
            bids = bids.filter(sub_contractor=request.query_params.get('sub'))
        if "primary" in request.query_params:
            bids = bids.filter(
                primary_contractor=request.query_params.get('primary'))
        if "job" in request.query_params:
            bids = bids.filter(job=request.query_params.get('job'))
        if "accepted" in request.query_params:
            bids = bids.filter(accepted=request.query_params.get('accepted'))
        if "request" in request.query_params:
            bids = bids.filter(is_request=request.query_params.get('request'))

        serializer = BidSerializer(bids, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        Summary:
            Retrieve a specific bid by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the bid to retrieve.

        Returns:
            Response: A serialized dictionary containing the bid's data and HTTP status 200 OK,
            or HTTP status 404 Not Found if the bid with the specified primary key does not exist.
        """
        try:
            bid = Bid.objects.get(pk=pk)
            serializer = BidSerializer(bid, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Bid.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """
        Summary:
            Create a new object using the request data

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the bid to retrieve.

        Returns:
            Response: A serialized dictionary containing the bid's data and HTTP status 201 Created.
        """
        sub_contractor = Contractor.objects.get(user=request.data["sub"])
        primary_contractor = Contractor.objects.get(
            user=request.data["primary"])
        job = Job.objects.get(pk=request.data["job"])

        bid = Bid.objects.create(
            rate=request.data["rate"],
            accepted=False,
            job=job,
            sub_contractor=sub_contractor,
            primary_contractor=primary_contractor,
            is_request=request.data["is_request"],
        )

        serializer = BidSerializer(bid, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """
        Summary:
            Update a specific bid's user information by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the bid to update.

        Returns:
            Response: A successful HTTP status 204 No Content response after updating the bid's user details,
            or HTTP status 404 Not Found if the bid with the specified primary key does not exist.
        """
        try:
            bid = Bid.objects.get(pk=pk)
            bid.job = Job.objects.get(pk=request.data["job"])
            bid.sub_contractor = Contractor.objects.get(pk=request.data["sub"])
            bid.primary_contractor = Contractor.objects.get(
                pk=request.data["primary"])
            bid.rate = request.data["rate"]
            bid.accepted = request.data["accepted"]
            bid.is_request = request.data["is_request"]
            bid.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Bid.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """
        Summary:
            Delete a specific bid and associated user by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the bid to delete.

        Returns:
            Response: A successful HTTP status 204 No Content response after deletion,
            or HTTP status 404 Not Found if the bid with the specified primary key does not exist.
        """

        try:
            bid = Bid.objects.get(pk=pk)
            bid.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Bid.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('id', 'name', 'contractor_id', 'complete', 'open')


class ContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contractor
        fields = ('id', 'company_name',)


class BidSerializer(serializers.ModelSerializer):

    job = JobSerializer(many=False)
    primary_contractor = ContractorSerializer(many=False)
    sub_contractor = ContractorSerializer(many=False)

    class Meta:
        model = Bid
        fields = ('id', 'rate', 'job', 'primary_contractor',
                  'sub_contractor', 'accepted', 'is_request',)

from django.db import models


class Bid(models.Model):
    rate = models.FloatField(null=True, blank=True)
    job_field = models.ForeignKey(
        "JobField", on_delete=models.CASCADE, related_name="bid")
    primary_contractor = models.ForeignKey(
        "Contractor", on_delete=models.CASCADE, related_name="my_requests")
    sub_contractor = models.ForeignKey(
        "Contractor", on_delete=models.CASCADE, related_name="my_bids")
    accepted = models.BooleanField(default=False)
    is_request = models.BooleanField(default=False)

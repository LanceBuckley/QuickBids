from django.db import models


class Bid(models.Model):
    rate = models.FloatField
    job = models.ForeignKey(
        "Job", on_delete=models.CASCADE, related_name="bids")
    contractor = models.ForeignKey(
        "Contractor", on_delete=models.CASCADE, related_name="my_bids")
    accepted = models.BooleanField

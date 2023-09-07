from django.db import models


class Job(models.Model):
    contractor = models.ForeignKey(
        "Contractor", on_delete=models.CASCADE, related_name="my_jobs")
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    field = models.CharField(max_length=50)
    blueprint = models.ImageField
    square_footage = models.FloatField
    open = models.BooleanField
    complete = models.BooleanField

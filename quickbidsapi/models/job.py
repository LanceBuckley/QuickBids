from django.db import models


class Job(models.Model):
    contractor = models.ForeignKey(
        "Contractor", on_delete=models.CASCADE, related_name="my_jobs")
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    fields = models.ManyToManyField("Field", through='JobField')
    square_footage = models.FloatField(null=True, blank=True)
    open = models.BooleanField(null=True, blank=True)
    complete = models.BooleanField(null=True, blank=True)

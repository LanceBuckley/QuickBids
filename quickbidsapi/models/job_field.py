from django.db import models


class JobField(models.Model):
    job = models.ForeignKey("Job", on_delete=models.CASCADE, related_name="applicable_fields")
    field = models.ForeignKey("Field", on_delete=models.CASCADE, related_name="applicable_jobs")

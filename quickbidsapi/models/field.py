from django.db import models


class Field(models.Model):
    job_title = models.CharField(max_length=50)

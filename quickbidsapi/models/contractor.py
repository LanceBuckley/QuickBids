from django.db import models
from django.contrib.auth.models import User


class Contractor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=10)
    primary_contractor = models.BooleanField(default=False)

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Users(AbstractUser):
    phone = models.CharField(max_length=11)

    class Meta:
        db_table = 'Users'

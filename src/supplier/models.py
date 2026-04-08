from django.db import models

from core.models import BaseModel

class Supplier(BaseModel):
    name = models.CharField(max_length=200, unique=True)
    founded_year = models.PositiveIntegerField()
    contact_email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
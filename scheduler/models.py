from django.db import models
from django.db.models.fields import uuid

# Create your models here.
class Schedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    payload = models.JSONField()
    cron_expression = models.CharField(max_length=128) 

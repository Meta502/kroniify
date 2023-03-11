from django.db import models
from django.db.models.fields import uuid
from django.utils import timezone
from pyawscron import AWSCron
from utils.schedule_event import schedule_event
from utils.unschedule_event import unschedule_event

# Create your models here.
class Schedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    payload = models.JSONField()
    cron_expression = models.CharField(max_length=128)
    target_url = models.URLField()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        schedule_event(self.id, self.cron_expression)

    def delete(self):
        super().delete()
        unschedule_event(self.id)

    def __str__(self):
        try:
            next_occurrence = AWSCron.get_next_n_schedule(1, timezone.now(), self.cron_expression)[0]
            return f"{self.id} - {self.target_url} - Next Occurrence: {next_occurrence}"
        except:
            return f"{self.id} - Invalid Cron Expression"

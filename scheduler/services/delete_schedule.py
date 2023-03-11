from django.urls.converters import uuid

from scheduler.models import Schedule


class DeleteScheduleService:
    @classmethod
    def run(cls, id: uuid.UUID):
        Schedule.objects.filter(id=id).delete()


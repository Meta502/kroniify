from django.apps import AppConfig

from utils.schedule_event import schedule_event


class SchedulerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduler'

    def ready(self):
        try:
            Schedule = self.get_model('Schedule')
            all_schedules = Schedule.objects.all()
            for schedule in all_schedules:
                schedule_event(schedule.id, schedule.cron_expression)
        except:
            print("Failed to initialize schedules on Redis")

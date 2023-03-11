from drf_yasg.utils import status, swagger_auto_schema
from rest_framework.response import Response
from rest_framework.schemas.coreapi import serializers
from rest_framework.views import APIView
from rest_framework import permissions
from scheduler.models import Schedule

from scheduler.services.create_schedule import CreateScheduleService

class ListCreateScheduleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    class CreateScheduleRequestSerializer(serializers.Serializer):
        target_url = serializers.URLField()
        payload = serializers.JSONField()
        cron_expression = serializers.RegexField(regex="((((\d+,)+\d+|(\d+(\/|-)\d+)|\d+|\*) ?){5,7})")

    class CreateScheduleResponseSerializer(serializers.Serializer): 
        id = serializers.UUIDField()
        payload = serializers.JSONField()
        cron_expression = serializers.CharField()
        next_occurrences = serializers.ListSerializer(child=serializers.DateTimeField())

    class ListScheduleResponseSerializer(serializers.Serializer):
        class ScheduleSerializer(serializers.Serializer):
            id = serializers.UUIDField()
            payload = serializers.JSONField()
            cron_expression = serializers.CharField()
            target_url = serializers.URLField()

        schedules = serializers.ListSerializer(child=ScheduleSerializer())

    @swagger_auto_schema(
        request_body=CreateScheduleRequestSerializer(),
        responses={
            "201": CreateScheduleResponseSerializer(), 
        },
        tags=["Scheduler"],
    )
    def post(self, request):
        serializer = self.CreateScheduleRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        schedule = CreateScheduleService.run(user=request.user, **serializer.data)

        return Response(self.CreateScheduleResponseSerializer(schedule).data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        responses={
            "200": ListScheduleResponseSerializer(),
        }
    )
    def get(self, request):
        schedules = Schedule.objects.filter(user=request.user)

        return Response(
            self.ListScheduleResponseSerializer({
                "schedules": schedules,
            }).data
        )
        

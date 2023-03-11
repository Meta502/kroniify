from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.schemas.coreapi import serializers
from rest_framework.views import APIView
from rest_framework import permissions

import re

from scheduler.services.create_schedule import CreateScheduleService

class CreateScheduleView(APIView):
    permission_classes = [permissions.AllowAny]

    class CreateScheduleRequestSerializer(serializers.Serializer):
        target_url = serializers.URLField()
        payload = serializers.JSONField()
        cron_expression = serializers.RegexField(regex="((((\d+,)+\d+|(\d+(\/|-)\d+)|\d+|\*) ?){5,7})")

    class CreateScheduleResponseSerializer(serializers.Serializer): 
        id = serializers.UUIDField()
        payload = serializers.JSONField()
        cron_expression = serializers.CharField()
        next_occurrences = serializers.ListSerializer(child=serializers.DateTimeField())
        
    class EditScheduleRequestSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        target_url = serializers.URLField()
        payload = serializers.JSONField()
        cron_expression = serializers.CharField()

    @swagger_auto_schema(
        request_body=CreateScheduleRequestSerializer(),
        responses={
            "200": CreateScheduleResponseSerializer(), 
        },
        tags=["Scheduler"],
    )
    def post(self, request):
        serializer = self.CreateScheduleRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        schedule = CreateScheduleService.run(**serializer.data)

        return Response(self.CreateScheduleResponseSerializer(schedule).data)

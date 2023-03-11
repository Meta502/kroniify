from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.schemas.coreapi import serializers
from rest_framework.views import APIView
from rest_framework import permissions

from scheduler.services.create_schedule import CreateScheduleService

class ScheduleView(APIView):
    permission_classes = [permissions.AllowAny]

    class CreateScheduleRequestSerializer(serializers.Serializer):
        target_url = serializers.URLField()
        payload = serializers.JSONField()
        cron_expression = serializers.CharField()

    class CreateScheduleResponseSerializer(serializers.Serializer): 
        id = serializers.UUIDField()
        payload = serializers.JSONField()
        cron_expression = serializers.CharField()
        next_occurrences = serializers.ListSerializer(child=serializers.DateTimeField())
        
    
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


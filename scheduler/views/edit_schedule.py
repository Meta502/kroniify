from django.db.models.fields import uuid
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.schemas.coreapi import serializers
from rest_framework.views import APIView
from rest_framework import permissions

from scheduler.services.edit_schedule import EditScheduleService

class EditScheduleView(APIView):
    permission_classes = [permissions.AllowAny]

    class EditScheduleRequestSerializer(serializers.Serializer):
        target_url = serializers.URLField(allow_blank=True, allow_null=True)
        payload = serializers.JSONField(allow_null=True)
        cron_expression = serializers.CharField(allow_blank=True, allow_null=True)

    class EditScheduleResponseSerializer(serializers.Serializer): 
        id = serializers.UUIDField()
        payload = serializers.JSONField()
        cron_expression = serializers.CharField()
        next_occurrences = serializers.ListSerializer(child=serializers.DateTimeField())

    @swagger_auto_schema(
        request_body=EditScheduleRequestSerializer(),
        responses={
            "200": EditScheduleResponseSerializer(), 
        },
        tags=["Scheduler"],
    )
    def put(self, request, schedule_id: uuid.UUID):
        serializer = self.EditScheduleRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        edited_schedule = EditScheduleService.run(id=schedule_id, data=serializer.data)

        return Response(
            self.EditScheduleResponseSerializer(edited_schedule).data
        )

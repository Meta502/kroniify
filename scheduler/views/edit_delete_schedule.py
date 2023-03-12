from django.db.models.fields import uuid
from drf_yasg.utils import status, swagger_auto_schema
from rest_framework.response import Response
from rest_framework.schemas.coreapi import serializers
from rest_framework.views import APIView
from rest_framework import permissions
from scheduler.services.delete_schedule import DeleteScheduleService

from scheduler.services.edit_schedule import EditScheduleService

class EditDeleteScheduleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

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
            "201": EditScheduleResponseSerializer(), 
        },
        tags=["Scheduler"],
    )
    def put(self, request, schedule_id: uuid.UUID):
        serializer = self.EditScheduleRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        edited_schedule = EditScheduleService.run(id=schedule_id, data=serializer.data)

        return Response(
            self.EditScheduleResponseSerializer(edited_schedule).data,
            status=status.HTTP_201_CREATED
        )

    @swagger_auto_schema(
        responses={
            "204": None
        },
        tags=["Scheduler"]
    )
    def delete(self, request, schedule_id: uuid.UUID):
        DeleteScheduleService.run(schedule_id)

        return Response(status=status.HTTP_204_NO_CONTENT)
        

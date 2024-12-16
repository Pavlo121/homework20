from rest_framework import serializers
from django.contrib.auth.models import User
from datetime import date

class TaskSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(required=False)
    due_date = serializers.DateField(required=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    def validate_due_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Дата завершення не може бути в минулому.")
        return value

    def validate_user(self, value):
        if value is not None and (not value.username or not value.email):
            raise serializers.ValidationError("Користувач повинен мати ім'я та електронну пошту.")
        return value

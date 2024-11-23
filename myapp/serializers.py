from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'fullname',
            'mobile_number',
            'dob',
            'profile',
            'career_path',
            'high_light',
            'focus',
            'years_of_experience',
            'department',
            'schedule',
            'is_doctor',
        ]

from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password')

    def validate_email(self, value):
        email = value.strip().lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email is already in use')
        return email

    def create(self, validated_data):
        name = validated_data.pop('name')
        email = validated_data['email']

        user = User.objects.create_user(
            username=email,
            email=email,
            password=validated_data['password'],
            first_name=name
        )
        return user

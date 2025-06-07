# Serializers turn your Django model into JSON (the data format used in APIs) and back.

from rest_framework import serializers
from .models import User, ConnectionRequest, GenderEnum, ConnectionStatusEnum

# use this serializer for model serializer but it doesnt align with cassandra
# class UserSerializer (serializers.ModelSerializer):
#   class Meta: 
#     model = User
#     fields = "__all__"

# use this serializer for cassandra
class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    age = serializers.IntegerField(required=False)
    gender = serializers.ChoiceField(choices=[(e.value, e.value) for e in GenderEnum], required=False)
    photo_url = serializers.CharField(max_length=500, required=False)
    skills = serializers.ListField(child=serializers.CharField(), required=False)
    location = serializers.CharField(max_length=255, required=False)
    interests = serializers.ListField(child=serializers.CharField(), required=False)
    education = serializers.ListField(child=serializers.CharField(), required=False)
    work = serializers.ListField(child=serializers.CharField(), required=False)
    bio = serializers.CharField(max_length=1000, required=False)
    hobbies = serializers.ListField(child=serializers.CharField(), required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        return User.create(**validated_data)
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class ConnectionRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    from_user_id = serializers.UUIDField()
    to_user_id = serializers.UUIDField()
    status = serializers.ChoiceField(choices=[(e.value, e.value) for e in ConnectionStatusEnum])
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        return ConnectionRequest.create(**validated_data)
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
# backend/api/serializers.py

from rest_framework import serializers
from .models import User, Document

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'role')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data['role'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class DoctorDocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['file', 'type', 'patient']
        
    def get_qr_code_url(self, obj):
        if obj.qr_code:
            return obj.qr_code.url
        return None


    def validate(self, data):
        uploader = self.context['request'].user
        if uploader.role != 'doctor':
            raise serializers.ValidationError("Only doctors are allowed to upload documents.")
        return data

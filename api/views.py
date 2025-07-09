
# backend/api/views.py

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import User, Document
from .serializers import RegisterSerializer, DoctorDocumentUploadSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .utils import generate_qr_code

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['role'] = user.role
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class DoctorDocumentUploadView(generics.CreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DoctorDocumentUploadSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        uploader = self.request.user
        if uploader.role != 'doctor':
            raise PermissionError("Only doctors can upload documents.")

        document = serializer.save(uploaded_by=uploader)

        qr_path = generate_qr_code(str(document.doc_uid))
        document.qr_code.name = qr_path.replace('/media/', '')  # Store relative path
        document.save()



# backend/api/views.py

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import User, Document
from .serializers import RegisterSerializer, DoctorDocumentUploadSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .utils import generate_qr_code
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from .models import Document
from django.contrib.auth import get_user_model
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()

@csrf_exempt
def verify_document(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            doc_id = data.get("doc_id")
            if not doc_id:
                return JsonResponse({"success": False, "error": "Missing document ID."}, status=400)

            doc = Document.objects.filter(doc_uid=doc_id).first()
            if not doc:
                return JsonResponse({"success": False, "error": "Document not found."}, status=404)

            return JsonResponse({
                "success": True,
                "file_url": doc.file.url,
                "file_name": doc.file.name,
                "type": doc.type
            })
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    return JsonResponse({"success": False, "error": "Invalid request method."}, status=405)

@login_required
def upload_document(request):
    if request.method == "POST":
        file = request.FILES.get("document")
        patient_id = request.POST.get("patient")
        doc_type = request.POST.get("type")

        try:
            patient = User.objects.get(id=patient_id)
            Document.objects.create(
                uploaded_by=request.user,
                patient=patient,
                file=file,
                type=doc_type
            )
            return redirect("scan_page")
        except Exception as e:
            return render(request, "upload.html", {"error": str(e)})

    patients = User.objects.filter(role="patient")
    return render(request, "upload.html", {"patients":patients})

def scan_page(request):
    return render(request, 'scan.html')

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

        document = serializer.save(uploaded_by=self.request.user)
        doc_uid = document.doc_uid
        qr_path = generate_qr_code(doc_uid)
        document.qr_code = qr_path
        document.save()
        
class ScanDocumentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, doc_uid):
        user = request.user

        # Ensure only doctors can scan documents
        if user.role != 'doctor':
            return Response({"error": "Only doctors can scan documents."}, status=status.HTTP_403_FORBIDDEN)

        # Get the document or return 404
        document = get_object_or_404(Document, doc_uid=doc_uid)
        
         # Check if this doctor uploaded the document
        if document.uploaded_by != user:
            return Response({"error": "Access denied. You did not upload this document."}, status=status.HTTP_403_FORBIDDEN)

        # Serialize and return the document info
        serializer = DoctorDocumentUploadSerializer(document)
        return Response(serializer.data, status=status.HTTP_200_OK)



# backend/api/urls.py

from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView, DoctorDocumentUploadView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('upload/', DoctorDocumentUploadView.as_view(), name='doctor-upload'),
]

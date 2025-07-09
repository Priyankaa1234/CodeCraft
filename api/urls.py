# backend/api/urls.py

from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView, DoctorDocumentUploadView
from .views import ScanDocumentView
from .views import scan_page
from .views import scan_page, verify_document


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('upload/', DoctorDocumentUploadView.as_view(), name='doctor-upload'),
    path('scan/<uuid:doc_uid>/', ScanDocumentView.as_view(), name='scan-document'),
    path('scan-page/', scan_page, name='scan_page'),
    path('verify-document/', verify_document, name='verify_document'),

]

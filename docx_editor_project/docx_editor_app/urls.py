from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('CertificateGenerator', views.index, name='index'),
    path('download_pdf/<str:pdf_output_filename>/', views.download_pdf, name='download_pdf'),
    path('validate_certificate/', views.validate_certificate, name='validate_certificate'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

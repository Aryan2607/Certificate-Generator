# docx_editor_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import os
import sys
import pythoncom
import atexit

if 'win32com.shell' not in sys.modules:
    pythoncom.CoInitialize()

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('docx_editor_app.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 'win32com.shell' in sys.modules:
    atexit.register(pythoncom.CoUninitialize)
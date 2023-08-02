from docxtpl import DocxTemplate
from docx2pdf import convert
from django.conf import settings
import os
import pythoncom
from django.http import HttpResponse,Http404
from django.shortcuts import render, redirect
from .models import GeneratedCertificate
import random
import string

def homepage(request):
    return render(request, 'homepage.html')

def validate_certificate(request):
    if request.method == 'POST':
        certificate_id = request.POST.get('certificate_id')
        try:
            generated_certificate = GeneratedCertificate.objects.get(certificate_id=certificate_id)
            # Certificate ID is valid, you can do any additional processing here if needed
            context = {
                'certificate_id': generated_certificate.certificate_id,
                'name': generated_certificate.name,
                'paragraph': generated_certificate.paragraph,
                'certificate_type': generated_certificate.certificate_type,
                'date': generated_certificate.date,
                'signature': generated_certificate.signature,
                'selected_template_id': generated_certificate.selected_template_id,
            }
            return render(request, 'certificate_validated.html', context)
        except GeneratedCertificate.DoesNotExist:
            # Certificate ID is not valid
            error_message = 'Invalid certificate ID. Please try again.'
            return render(request, 'validate_certificate.html', {'error_message': error_message})
    else:
        return render(request, 'validate_certificate.html')

def index(request):
    if request.method == 'POST':

        pythoncom.CoInitialize()
        name = request.POST.get('name', '')
        paragraph = request.POST.get('paragraph', '')
        certificate_type = request.POST.get('certificate_type', '')
        date = request.POST.get('date', '')
        signature = request.POST.get('signature', '')
        selected_template_id = request.POST.get('template_id', 'template1')

        data_to_save = GeneratedCertificate(
            name = request.POST.get('name', ''),
            paragraph = request.POST.get('paragraph', ''),
            certificate_type = request.POST.get('certificate_type', ''),
            date = request.POST.get('date', ''),
            signature = request.POST.get('signature', ''),
            selected_template_id = request.POST.get('template_id', 'template1'),
        )
        data_to_save.save()
        # Generate a unique ID for the certificate
        certificate_id = data_to_save.certificate_id

        # Map the selected template ID to the actual template file path
        template_paths = {
            'template1': os.path.join(settings.BASE_DIR, 'docx_editor_app/templates/template1.docx'),
            'template2': os.path.join(settings.BASE_DIR, 'docx_editor_app/templates/template2.docx'),
        }

        # Load the DOCX template
        template_file_path = template_paths.get(selected_template_id)
        doc = DocxTemplate(template_file_path)

        # Data to replace placeholders in the DOCX template
        context = {
            'NAME': name,
            'PARAGRAPH': paragraph,
            'CERTIFICATE_TYPE': certificate_type,
            'DATE': date,
            'SIGNATURE': signature,
            'ID': certificate_id,
        }

        # Replace placeholders in the DOCX template with user inputs
        doc.render(context)

        # Save the edited DOCX file with a unique name
        output_filename = f'generated_certificate_{name}.docx'
        output_filepath = os.path.join(settings.MEDIA_ROOT, output_filename)
        doc.save(output_filepath)

        # Convert the DOCX file to PDF
        pdf_output_filepath = os.path.splitext(output_filepath)[0] + '.pdf'
        convert(output_filepath, pdf_output_filepath)

        pythoncom.CoUninitialize()

        # Redirect the user to the generated PDF file directly
        pdf_output_filename = os.path.basename(pdf_output_filepath)
        return redirect('download_pdf', pdf_output_filename)
    return render(request, 'index.html')

def download_pdf(request, pdf_output_filename):
    pdf_output_filepath = os.path.join(settings.MEDIA_ROOT, pdf_output_filename)
    if not os.path.exists(pdf_output_filepath):
        raise Http404

    with open(pdf_output_filepath, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{pdf_output_filename}"'
        return response
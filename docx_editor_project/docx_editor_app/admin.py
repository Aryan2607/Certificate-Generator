from django.contrib import admin
from .models import GeneratedCertificate
from django.http import HttpResponse, FileResponse

import os
from django.conf import settings
from docxtpl import DocxTemplate
from docx2pdf import convert
import pythoncom

def print_certificate(modeladmin, request, queryset):
    for certificate in queryset:
        # Generate PDF for each selected certificate and save to temp directory
        pythoncom.CoInitialize()

        # Map the selected template ID to the actual template file path
        template_paths = {
            'template1': os.path.join(settings.BASE_DIR, 'docx_editor_app/templates/template1.docx'),
            'template2': os.path.join(settings.BASE_DIR, 'docx_editor_app/templates/template2.docx'),
        }

        # Load the DOCX template
        selected_template_id = certificate.selected_template_id
        template_file_path = template_paths.get(selected_template_id)
        doc = DocxTemplate(template_file_path)

        # Data to replace placeholders in the DOCX template
        context = {
            'NAME': certificate.name,
            'PARAGRAPH': certificate.paragraph,
            'CERTIFICATE_TYPE': certificate.certificate_type,
            'DATE': certificate.date,
            'SIGNATURE': certificate.signature,
        }

        # Replace placeholders in the DOCX template with user inputs
        doc.render(context)

        # Save the edited DOCX file with a unique name
        output_filename = f'generated_certificate_{certificate.name}.docx'
        output_filepath = os.path.join(settings.MEDIA_ROOT, output_filename)
        doc.save(output_filepath)

        # Convert the DOCX file to PDF
        pdf_output_filepath = os.path.splitext(output_filepath)[0] + '.pdf'
        convert(output_filepath, pdf_output_filepath)

        pythoncom.CoUninitialize()

        # Download the generated PDF for the selected certificate
        with open(pdf_output_filepath, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{pdf_output_filepath}"'
            return response

    # Return None in case of error
    return None

@admin.register(GeneratedCertificate)
class GeneratedCertificateAdmin(admin.ModelAdmin):
    # Display additional columns in the admin table
    list_display = ['name', 'paragraph', 'certificate_type', 'date', 'signature','certificate_id']

    # Add the custom action 'print_certificate' to the admin actions
    actions = [print_certificate]

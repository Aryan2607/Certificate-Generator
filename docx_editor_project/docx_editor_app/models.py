from django.db import models
import uuid
import random, string

def generate_certificate_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=20))

# Model for storing data from the HTML form
class GeneratedCertificate(models.Model):
    name = models.CharField(max_length=100)
    paragraph = models.TextField()
    certificate_type = models.CharField(max_length=50)
    date = models.DateField()
    signature = models.CharField(max_length=100)
    selected_template_id = models.CharField(max_length=10)
    certificate_id = models.CharField(max_length=10, default=generate_certificate_id, null=True, blank=True)
    # Add other fields as needed

    def save(self, *args, **kwargs):
        if not self.certificate_id:
            self.certificate_id = generate_certificate_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

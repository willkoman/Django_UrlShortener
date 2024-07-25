from io import BytesIO

import qrcode
from django.core.files.base import ContentFile
from django.db import models


class URL(models.Model):
    original_url = models.URLField()
    short_url = models.CharField(max_length=10, unique=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, null=True)
    num_of_visits = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        host_url = kwargs.pop('host_url', 'http://localhost:8000/')

        if not self.qr_code:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(f'{host_url}{self.short_url}')
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            file_name = f'{self.short_url}_qr.png'
            self.qr_code.save(file_name, ContentFile(buffer.getvalue()), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.short_url} -> {self.original_url}"

    class Meta:
        verbose_name = "URL"
        verbose_name_plural = "URLs"

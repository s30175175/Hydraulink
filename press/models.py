from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import models


class ShortURL(models.Model):
    slug = models.CharField(max_length=20, unique=True)
    original_url = models.URLField()
    password = models.CharField(max_length=128, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    utm_source = models.CharField(max_length=128, blank=True, null=True)
    utm_medium = models.CharField(max_length=128, blank=True, null=True)
    utm_campaign = models.CharField(max_length=128, blank=True, null=True)
    utm_term = models.CharField(max_length=128, blank=True, null=True)
    utm_content = models.CharField(max_length=128, blank=True, null=True)
    create_by = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name='shorturls'
    )
    click_count = models.PositiveBigIntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(blank=True, null=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

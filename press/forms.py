from django import forms

from .models import ShortURL


class ShortURLForm(forms.ModelForm):
    class Meta:
        model = ShortURL
        fields = [
            'slug',
            'original_url',
            'password',
            'note',
            'utm-source',
            'utm-medium',
            'utm-campaign',
            'utm-term',
            'utm-content',
        ]

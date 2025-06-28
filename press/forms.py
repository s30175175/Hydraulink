from django import forms

from .models import ShortURL


class ShortURLForm(forms.ModelForm):
    slug = forms.CharField(required=False)

    class Meta:
        model = ShortURL
        fields = [
            'slug',
            'original_url',
            'password',
            'note',
            'is_active',
        ]

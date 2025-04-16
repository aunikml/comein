from django import forms
from users.models import UserProfile

class CalendlyLinkForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['calendly_link']
        widgets = {
            'calendly_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://calendly.com/your-username/30min'
            })
        }
from django import forms
from .models import UserProfile
from django.contrib.auth import get_user_model
from django.forms import ModelForm

User = get_user_model()

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'bio',
            'cv',
            'preferred_research_methods',
            'image',
            'area_of_specialization',
            'research_interest',
            'publications',
            'conferences_workshops',
        ]

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})


class UserCreationAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(UserCreationAdminForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
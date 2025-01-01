from django import forms
from .models import UserProfile
from django.contrib.auth import get_user_model
from django.forms import ModelForm

User = get_user_model()

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'cv', 'preferred_research_methods', 'image']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['bio'].widget.attrs.update({'class': 'form-control'})
        self.fields['cv'].widget.attrs.update({'class': 'form-control'})
        self.fields['preferred_research_methods'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})


class UserCreationAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(UserCreationAdminForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
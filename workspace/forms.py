from django import forms
from .models import Resource, Chapter, Submission
from django.forms import ModelForm


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class ChapterForm(forms.ModelForm):
    deadline = forms.DateTimeField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Chapter
        fields = ['chapter_name', 'deadline']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

from django import forms
from .models import Resource, Chapter, Submission

# ... other forms

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['draft_number', 'file']

    def __init__(self, *args, **kwargs):
        super(SubmissionForm, self).__init__(*args, **kwargs)
        self.fields['draft_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['file'].widget.attrs.update({'class': 'form-control'})

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if not file.name.endswith(('.docx', '.pdf')):
                raise forms.ValidationError("Only .docx and .pdf files are allowed.")
        return file

class SubmissionApprovalForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['status', 'comment']

    def __init__(self, *args, **kwargs):
        super(SubmissionApprovalForm, self).__init__(*args, **kwargs)
        self.fields['status'].widget.attrs.update({'class': 'form-control'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control'})

class SubmissionReviewForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['status', 'comment', 'annotated_file']

    def __init__(self, *args, **kwargs):
        super(SubmissionReviewForm, self).__init__(*args, **kwargs)
        self.fields['status'].widget.attrs.update({'class': 'form-control'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control'})
        self.fields['annotated_file'].widget.attrs.update({'class': 'form-control'})
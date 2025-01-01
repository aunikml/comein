from django import forms
from .models import Post, Reply, Forum, ResourceLink
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'context']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),  # Apply Bootstrap styling
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ['title', 'description', 'participants']

    def __init__(self, *args, **kwargs):
        super(ForumForm, self).__init__(*args, **kwargs)
        self.fields['participants'].widget.attrs.update({'class': 'form-control'})

class ResourceLinkForm(forms.ModelForm):
    class Meta:
        model = ResourceLink
        fields = ['url', 'description']
        widgets = {
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }
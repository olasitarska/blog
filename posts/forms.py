from django import forms
from django.template.defaultfilters import slugify

from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content',)
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title of your post'}),
            'content': forms.Textarea(attrs={'placeholder': 'Start writing here..'}),
        }

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].error_messages = {'required': 'Title is required'}
        self.fields['content'].error_messages = {'required': 'Text is required'}

    def save(self, commit=True):
        post = super(PostForm, self).save(commit=False)
        post.author = self._user

        if not post.slug:
            post.slug = slugify(post.title)

        if commit:
            post.save()
        return post

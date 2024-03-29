from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'post_type',
            'post_category',
            'post_title',
            'post_text'
        ]
        


from django import forms
from .models import Post, Comment
from django.contrib.auth.models import User

class PostCreateForm(forms.ModelForm):
    title = content = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите название поста', 'rows':'1', 'cols':'10'}))
    content = content = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите содержание поста', 'rows':'4', 'cols':'50'}))
    class Meta:
        model = Post
        fields = (
            'title',
            'content'
        )


class CommentCreateForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Оставить комментарий', 'rows':'4', 'cols':'50'}))
    class Meta:
        model = Comment
        fields = ('content',)
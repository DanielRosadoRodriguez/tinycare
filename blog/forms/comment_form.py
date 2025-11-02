from django import forms
from ..models.comment_model import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
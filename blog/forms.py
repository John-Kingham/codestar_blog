from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """
    A form for entering blog post comments.

    Models:
        :model:`blog.Comment`
    """

    class Meta:
        model = Comment
        fields = ("body",)

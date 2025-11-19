from django import forms
from .models import CollaborateRequest


class CollaborateForm(forms.ModelForm):
    """A form for entering collaboration requests.

    Model:
        :model:`about.CollaborateRequest`
    """
    class Meta:
        model = CollaborateRequest
        fields = ("name", "email", "message")

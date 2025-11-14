from django.shortcuts import render
from .forms import CollaborateForm
from .models import About


# Create your views here.
def about_view(request):
    about = About.objects.first()
    collaborate_form = CollaborateForm()
    context = {
        "about": about,
        "collaborate_form": collaborate_form,
    }
    return render(request, "about/about.html", context)

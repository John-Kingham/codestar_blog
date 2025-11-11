from django.http import HttpResponse
from django.shortcuts import render
from .models import About


# Create your views here.
def about_view(request):
    about = About.objects.first()
    return render(request, "about/about.html", {"about": about})

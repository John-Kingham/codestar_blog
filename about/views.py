from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def test_about(request):
    return HttpResponse("The about page view is working.")

from django.http import HttpResponse
from .models import About


# Create your views here.
def about_view(request):
    about = About.objects.first()
    return HttpResponse("About: " + about.title)

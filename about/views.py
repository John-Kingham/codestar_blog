from django.contrib import messages
from django.shortcuts import render
from .forms import CollaborateForm
from .models import About


# Create your views here.
def about_view(request):
    about = About.objects.first()
    if request.method == "POST":
        save_collaboration_request(request)
    collaborate_form = CollaborateForm()
    context = {
        "about": about,
        "collaborate_form": collaborate_form,
    }
    return render(request, "about/about.html", context)


def save_collaboration_request(request):
    """
    Save a collaboration request to the database.
    If the request is successful, send a confirmation message to `messages`.

    Args:
        request (HTTPRequest): The HTTP request
    """
    collaboration_form = CollaborateForm(data=request.POST)
    if collaboration_form.is_valid():
        collaboration_request = collaboration_form.save(commit=False)
        collaboration_request.read = False
        collaboration_request.save()
        message = (
            "Collaboration request received! I endeavour to respond "
            "within 2 working days."
        )
        messages.add_message(request, messages.SUCCESS, message)

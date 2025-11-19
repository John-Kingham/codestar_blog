from django.contrib import messages
from django.shortcuts import render
from .forms import CollaborateForm
from .models import About


# Create your views here.
def about_view(request):
    """
    Return the About page and save collaboration requests.

    Return the About page with the latest content. If this is a POST request,
    the user has submitted a collaboration request, so add it to the database.

    Args:
        request (HttpRequest):
            A GET or POST request. If the request is a POST request, it
            contains :form:`about.CollaborateForm` data for a new collaboration
            request.

    Models:
        :model:`about.About`
        :model:`about.CollaborateRequest`

    Template:
        :template:`about/about.html`

    context:
        about (:model:`about.About`): The latest About content.
        collaborate_form (:form:`about.CollaborateForm`): An empty form.

    Messages:
        SUCCESS: If the collaborate request is saved to the database.
        ERROR: If the attempt to save the collaborate request fails.

    Returns:
        HttpResponse: Contains the about page.
    """
    about = About.objects.first()
    if request.method == "POST":
        _save_collaborate_request(request)
    collaborate_form = CollaborateForm()
    context = {
        "about": about,
        "collaborate_form": collaborate_form,
    }
    return render(request, "about/about.html", context)


def _save_collaborate_request(request):
    """
    Save a collaborate request to the database.

    Args:
        request (HttpRequest):
            A POST request containing :form:`about.CollaborateForm` data.

    Models:
        :model:`about.CollaborateRequest`

    Messages:
        SUCCESS: If the collaborate request is saved to the database.
        ERROR: If the attempt to save the collaborate request fails.
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
    else:
        message = "Error saving your collaboration request. Please try again."
        messages.add_message(request, messages.ERROR, message)

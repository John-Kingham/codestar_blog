from cloudinary.models import CloudinaryField
from django.db import models


class About(models.Model):
    """
    Content for the About page.
    """
    title = models.CharField(max_length=200, unique=True)
    profile_image = CloudinaryField("image", default="placeholder")
    content = models.TextField()
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-updated_on"]


class CollaborateRequest(models.Model):
    """
    A user request for collaboration.
    """
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Collaboration request from {self.name}"

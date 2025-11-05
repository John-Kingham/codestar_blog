from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Post


# Create your views here.
class PostList(generic.ListView):
    PUBLISHED = 1
    queryset = Post.objects.filter(status=PUBLISHED)
    template_name = "blog/index.html"
    paginate_by = 6

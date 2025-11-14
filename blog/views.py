from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views import generic
from .forms import CommentForm
from .models import Post, PUBLISHED


# Create your views here.
class PostList(generic.ListView):
    queryset = Post.objects.filter(status=PUBLISHED)
    template_name = "blog/index.html"
    paginate_by = 6


def post_detail(request, slug):
    """
    Display an individual :model:`blog.Post`.

    **Context**

    ``post``
        An instance of :model:`blog.Post`.

    **Template**

    :template:`blog/post_detail.html`
    """
    queryset = Post.objects.filter(status=PUBLISHED)
    post = get_object_or_404(queryset, slug=slug)
    comments = post.comments.all().order_by("-created_on")
    comment_count = post.comments.filter(approved=True).count()
    if request.method == "POST":
        save_comment(request, post)
    comment_form = CommentForm()
    context = {
        "post": post,
        "comments": comments,
        "comment_count": comment_count,
        "comment_form": comment_form,
    }
    return render(request, "blog/post_detail.html", context)


def save_comment(request, post):
    """
    Extract a `Comment` from a request and save it to the database.
    Adds a success message to `messages` if the save was successful.

    Args:
        request (HttpRequest): The HTTP request.
        post (Post): The `Comment`'s related blog post.
    """
    comment_form = CommentForm(data=request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        message = "Comment submitted and awaiting approval"
        messages.add_message(request, messages.SUCCESS, message)

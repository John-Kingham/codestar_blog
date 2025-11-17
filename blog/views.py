from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse
from django.views import generic
from .forms import CommentForm
from .models import Comment, Post, PUBLISHED


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
        _create_comment(request, post)
    comment_form = CommentForm()
    context = {
        "post": post,
        "comments": comments,
        "comment_count": comment_count,
        "comment_form": comment_form,
    }
    return render(request, "blog/post_detail.html", context)


def _create_comment(request, post):
    """
    Save a new comment to the database.

    If the comment data is valid, a database record is created for the comment
    and a success message is added to `messages`.

    Args:
        request (HttpRequest): A request containing valid comment data.
        post (Post): The comment's related blog post.
    """
    comment_form = CommentForm(data=request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        message = "Comment submitted and awaiting approval"
        messages.add_message(request, messages.SUCCESS, message)


def comment_edit(request, slug, comment_id):
    """
    Update a comment and reload post details after a comment has been edited.

    If the comment data is valid and the request's user is the comment author,
    then (a) the comment's database record is updated, (b) the comment's
    approved status is set to false, and (c) a success message is added to
    `messages`.

    Otherwise, an error message is added to `messages`.

    Args:
        request (HTTPRequest): A HTTP request containing valid data for the
            edited comment. The request's user is the comment's author.
        slug (str): A URL slug containing the ID of the edited comment's post.
        comment_id (int): The ID of the edited comment.
    """
    if request.method == "POST":
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_form = CommentForm(data=request.POST, instance=comment)
        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.approved = False
            comment.save()
            messages.add_message(request, messages.SUCCESS, "Comment updated.")
        else:
            message = "Error updating comment."
            messages.add_message(request, messages.ERROR, message)
    return HttpResponseRedirect(reverse("post_detail", args=[slug]))


def comment_delete(request, slug, comment_id):
    """
    Delete a comment and then reload the post details page.

    Args:
        request (HTTPRequest): A request.
        slug (str): A URL slug containing the comment's blog post ID.
        comment_id (int): The comment's ID.
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, "Comment deleted.")
    else:
        message = "You can only delete your own comments."
        messages.add_message(request, messages.ERROR, message)
    return HttpResponseRedirect(reverse("post_detail", args=[slug]))

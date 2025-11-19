from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse
from django.views import generic
from .forms import CommentForm
from .models import Comment, Post, PUBLISHED


class PostList(generic.ListView):
    """
    A list view for blog posts.

    Models:
        :model:`blog.Post`

    Template:
        :template:`blog/index.html`

    Context:
        posts (QuerySet): All published posts.
    """

    queryset = Post.objects.filter(status=PUBLISHED)
    template_name = "blog/index.html"
    paginate_by = 6


def post_detail(request, slug):
    """
    Return the post details page for a post and save a new comment.

    If `request`'s method is POST, the user is trying to create a new comment,
    so save the comment to the database before returning the post details page.

    Args:
        request (HttpRequest):
            A GET or POST request. If it's a POST request, it contains
            :form:`blog.CommentForm` data for a new comment.
        slug (str): Contains the ID of a :model:`blog.Post`.

    Models:
        :model:`blog.Post`
        :model:`blog.Comment`

    Template:
        :template:`blog/post_detail.html`

    Context:
        post (:model:`blog.Post`): The blog post.
        comments (QuerySet): All :model:`blog.Comment` instances for the post.
        comment_count (int): The number of approved comments for the post.
        comment_form (:form:`blog.CommentForm`): An empty form.

    Messages:
        SUCCESS:
            If the request method is POST and if the new comment is saved
            to the database.
        ERROR:
            If the request method is POST and if there is an error saving
            the new comment to the database.

    Returns:
        HttpResponse: Contains the blog details page for the post.
    """
    published_posts = Post.objects.filter(status=PUBLISHED)
    post = get_object_or_404(published_posts, slug=slug)
    if request.method == "POST":
        _save_comment(request, post)
    context = {
        "post": post,
        "comments": post.comments.all().order_by("-created_on"),
        "comment_count": post.comments.filter(approved=True).count(),
        "comment_form": CommentForm(),
    }
    return render(request, "blog/post_detail.html", context)


def _save_comment(request, post):
    """
    Save a new comment to the database.

    Args:
        request (HttpRequest):
            A POST request. Contains :form:`blog.CommentForm` data for a new
            comment.
        post (:model:`blog.Post`): The new comment's related post.

    Models:
        :model:`blog.Comment`
        :model:`blog.Post`

    Messages:
        SUCCESS: If the new comment is saved to the database.
        ERROR: If there is an error saving the comment to the database.
    """
    comment_form = CommentForm(data=request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        message = "Comment submitted and awaiting approval"
        messages.add_message(request, messages.SUCCESS, message)
    else:
        message = "Error updating comment."
        messages.add_message(request, messages.ERROR, message)


def comment_edit(request, slug, comment_id):
    """
    Update an edited comment and reload the post details page.

    If the request's user is the comment's author, the comment's authorised
    status is set to false and its database record is updated.

    Args:
        request (HttpRequest):
            A POST request containing :form:`blog.CommentForm` data for the
            edited comment. The request's user is the comment's author.
        slug (str):
            A slug which is the ID of the edited comment's :model:`blog.Post`.
        comment_id (int): The ID of the edited comment.

    Models:
        :model:`blog.Comment`

    Template:
        :template:`blog/post_details.html`

    Messages:
        SUCCESS: If the edited comment is updated successfully.
        ERROR: If there is an error while attempting to update the database.

    Returns:
        HttpResponseRedirect:
            A redirect to the post details page for the comment's post.
    """
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

    If the request's user is the comment's author, delete the comment's
    database record.

    Args:
        request (HTTPRequest): A request where `user` is the comment's author.
        slug (str): A slug which is the comment's :model:`blog.Post` ID.
        comment_id (int): The comment's ID.

    Models:
        :model:`blog.Comment`

    Template:
        :template:`blog/post_details.html`

    Messages:
        SUCCESS: If the comment is deleted from the database.
        ERROR: If the request's user isn't the comment's author.

    Returns:
        HttpResponseRedirect:
            Redirect to the post details page for the comment's blog post.
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, "Comment deleted.")
    else:
        message = "You can only delete your own comments."
        messages.add_message(request, messages.ERROR, message)
    return HttpResponseRedirect(reverse("post_detail", args=[slug]))

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import Post

def post_list(request):

    if request.user.is_authenticated():
        post_list = Post.objects.all().order_by('-created_date')
    else:
        # If you're not an author, get only a list of published posts.
        post_list = Post.published.all().order_by('-published_date')

    # Pagination of posts
    paginator = Paginator(post_list, 3)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        post_list = paginator.page(paginator.num_pages)

    return render(request, 'posts/post_list.html', {
        'post_list': post_list
    })


def post_detail(request, post_pk, slug):

    if request.user.is_authenticated():
        post = get_object_or_404(Post, pk=post_pk)
    else:
        post = get_object_or_404(Post.published.all(), pk=post_pk)

    if post.slug != slug:
        return redirect('posts:post_detail', post_pk=post.pk, slug=post.slug)

    return render(request, 'posts/post_detail.html', {
        'post': post,
    })

@login_required
def post_toggle_publish(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if post.is_public():
        post.unpublish()
        messages.success(request, u'Your post has been unpublished.')
    else:
        post.publish()
        messages.success(request, u'Your post has been published!')

    return redirect('posts:post_detail',  post_pk=post.pk, slug=post.slug)

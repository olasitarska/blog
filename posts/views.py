from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

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

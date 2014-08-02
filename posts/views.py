from django.shortcuts import render

from .models import Post

def post_list(request):

    if request.user.is_authenticated():
        post_list = Post.objects.all().order_by('-created_date')
    else:
        post_list = Post.published.all().order_by('-published_date')

    return render(request, 'posts/post_list.html', {
        'post_list': post_list
    })

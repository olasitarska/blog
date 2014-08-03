from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('posts:post_list')
            else:
                messages.error(request, "Your account isn't active")
        else:
            messages.error(request, "Credentials are invalid")

    return render(request, 'users/login.html', {
    })

@login_required
def logout_view(request):
    logout(request)

    return redirect('posts:post_list')

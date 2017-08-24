from __future__ import unicode_literals, absolute_import

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from customer.forms import SignUpForm


def login(request):
    template_name = "frontend/login.html"
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None and user.is_active:
            auth_login(request, user)
            return HttpResponseRedirect("dashboard/")
        else:
            return render(request, template_name, {'error_message': 'Invalid login'})
    return render(request, template_name)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return HttpResponseRedirect("dashboard/")
    else:
        form = SignUpForm()
    return render(request, 'frontend/signup.html', {'form': form})


@login_required
def dashboard(request):
    if not request.user.is_authenticated():
        return render(request, "frontend/login.html")
    else:
        user = request.user
        return render(request, 'frontend/index.html', {'user': user})


@login_required
def logout(request):
    auth_logout(request)
    return render(request, "frontend/login.html", {"message": "You successfully logged out"})

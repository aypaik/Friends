from __future__ import unicode_literals
from ..login_app.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.

def dashboard(request):
    context = {
        'user_all':User.objects.exclude(id = request.session['id']),
        'user_logged':User.objects.get(id = request.session['id']),
    }
    if 'email' not in request.session:
        return redirect('/')
    return render(request, 'main_app/dashboard.html', context)

def add(request, id):
    logged_user = User.objects.get(id = request.session['id'])
    other_user = User.objects.get(id = id)
    logged_user.friends.add(other_user)
    return redirect('/main/dashboard')

def show(request, id):
    context = {
        'showuser':User.objects.get(id=id)
    }
    return render(request, 'main_app/show.html', context)

def remove(request, id):
    logged_user = User.objects.get(id = request.session['id'])
    other_user = User.objects.get(id = id)
    logged_user.friends.remove(other_user)
    return redirect('/main/dashboard')


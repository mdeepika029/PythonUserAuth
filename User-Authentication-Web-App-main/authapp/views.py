import json
import os
from django.http import request
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from src.settings import MEDIA_ROOT
from .forms import UserRegistration, UserEditForm
from django.core.files.storage import FileSystemStorage
import pdb as bp
from .models import UserDetails

from pdb import set_trace as bp


# Create your views here.

@login_required
def dashboard(request):
    context = {
        "welcome": "Welcome to your dashboard"
    }
    return render(request, 'authapp/dashboard.html', context=context)


def register(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(
                form.cleaned_data.get('password')
            )
            new_user.save()
            return render(request, 'authapp/register_done.html')
    else:
        form = UserRegistration()

    context = {
        "form": form
    }

    return render(request, 'authapp/register.html', context=context)


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    context = {
        'form': user_form,
    }
    return render(request, 'authapp/edit.html', context=context)


def simple_upload(request):
    
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        # print(os.getcwd())
        with open(f'{MEDIA_ROOT}/{filename}', 'r') as data:
            parsed_json = json.load(data)

        for result in parsed_json:
            UserDetails.objects.create(
           idValue = result['id'],
           userId = result['userId'],
           title=result['title'],
           body = result['body'], 
         ) 

        return render(request, 'authapp/dashboard.html', {
            'uploaded_file_url': uploaded_file_url,
            'parsed_json':parsed_json
        })
    return render(request, 'authapp/dashboard.html')




def fetch_data(request):
    
    query_data = UserDetails.objects.filter().values()
    return render(request, 'authapp/dashboard.html', {
            'data_fetched':query_data
        })
   
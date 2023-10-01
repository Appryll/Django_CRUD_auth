from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import CreateTaskForm
from .models import Task

from django.http import HttpResponse

# Create your views here.

# def helloworld(request):
#     return HttpResponse('Hello World')

# def signup(request):
#     return render(request, 'signup.html')
def home(request):
    return render(request, 'home.html', {
        # user name
        'username': request.user
    })    

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
        'form': UserCreationForm,
    })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # register user
                user = User.objects.create_user(
                    username=request.POST['username'], 
                    password=request.POST['password1'])
                user.save()
                #cookie auth user
                login(request, user)
                return redirect('task')
            except IntegrityError:
                # msg error
                return render(request, 'signup.html',{
                    'form': UserCreationForm,
                    'msg': 'User already exists'
                })
        else:
            return render(request, 'signup.html',{
                    'form': UserCreationForm,
                    'msg': 'Password do not match'
                })

def task(request):
    #list of tasks when they need to be completed
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request, 'task.html',{
        'tasks': tasks
    })

def signout(request):
    logout(request)
    return redirect ('home')

def signin(request):
    if request.method == 'GET':

        return render(request, 'signin.html', {
            'form': AuthenticationForm,
        })
    else:
        user = authenticate(request, 
                     username=request.POST['username'],
                     password=request.POST['password'])
        # if user is not in bdd
        if user is None:
            return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'msg': 'Username or password is incorrect'
        })
        else:
            login(request, user)
            return redirect('task')
        
def created_task(request):
    if request.method == 'ǴET':
        return render(request, 'created_task.html',{
            'form': CreateTaskForm
        })
    else:
        try:
            #crea un forñulario repleto
            form = CreateTaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user= request.user
            new_task.save()
            return redirect('task')
        # no cumple con requerimientos del formulario
        except ValueError:
            return render(request, 'created_task.html',{
            'form': CreateTaskForm,
            'msg': 'Please provide valida data'
        })

def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'task_detail.html', {
        'task': task 
    })



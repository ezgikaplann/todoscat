from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import todo
from .models import todo_grup
from django.contrib.auth.decorators import login_required
import datetime
# Create your views here.
@login_required
def home(request):
    if request.method == 'POST':
        grup = request.POST.get('grup')
        if grup != '' and todo_grup.objects.filter(user = request.user, grup_name = grup).exists() == False:    
            new_todo = todo_grup.objects.create(user = request.user, grup_name = grup)
            new_todo.save()
    all_grups = todo_grup.objects.filter(user = request.user)
    context = {
        'grups' : all_grups
    }
    
    return render(request, 'todo.html',context)    

@login_required
def listgrup(request, name):
    getgrup = todo_grup.objects.get(user = request.user, grup_name = name)
    if request.method == 'POST':
        task = request.POST.get('task')
        new_todo = todo.objects.create(user = request.user, grup = getgrup, todo_name = task)
        new_todo.save()
    
    print(getgrup.id)
    get_todos = todo.objects.filter(user = request.user, grup = getgrup.id)
    context = {
        'todos' : get_todos
    }

    return render(request, 'list.html',context)

def register(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if len(password) < 4:
            messages.error(request, 'Password too short')
            return redirect('register')
        if User.objects.filter(username = username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        
        new_user = User.objects.create_user(username = username, email = email, password = password)
        new_user.save()
        print('user created')
        print(username, password, email)
        messages.success(request, 'Account created successfully')
        return redirect('login')
    else:
        return render(request, 'register.html',{})
    

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home-page')
        else:
            messages.error(request, 'Username or password is incorrect')
            return redirect('login')
    return render(request, 'login.html',{})

@login_required
def DeleteTask(request, name):
    get_todo = todo.objects.get(user = request.user, todo_name = name)
    get_todo.delete()
    return redirect('listgrup', get_todo.grup.grup_name)

@login_required
def Update(request, name):
    get_todo = todo.objects.get(user = request.user, todo_name = name)
    get_todo.status = not get_todo.status
    get_todo.end_date = datetime.date.today()
    get_todo.save()
    return redirect('listgrup', get_todo.grup.grup_name)


def LogoutView(request):
    logout(request)
    return redirect('login')
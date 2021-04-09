from django.shortcuts import render, redirect
import bcrypt
from .models import * 
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def create_user(request):
    if request.method == "POST":
        errors = User.objects.create_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(name=request.POST['user_name'], alias=request.POST['alias'], email=request.POST['email'], password=pw_hash)
            request.session['user_id'] = user.id
            return redirect('/ideas_page')
    return redirect('/')

def ideas(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
        'all_ideas': Idea.objects.all()
        }
    return render(request, "ideas.html", context)

def login(request):
    if request.method == "POST":
        users_with_email = User.objects.filter(email=request.POST['email'])
        if users_with_email:
            user = users_with_email[0]
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id
                return redirect('/ideas_page')
        messages.error(request, "Email or password is incorrect") 
    return redirect('/') 

def create_idea(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == "POST":
        errors = Idea.objects.create_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/ideas_page')
        else:
            idea = Idea.objects.create(description=request.POST['description'], creator=User.objects.get(id=request.session['user_id']))
            return redirect('/ideas_page')
    return redirect('/ideas_page')

def logout(request):
    request.session.flush()
    return redirect('/')




# Create your views here.

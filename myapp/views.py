from django.shortcuts import render, redirect
from .models import hsk as list_hsk
from django.contrib.auth.forms import UserCreationForm
from .form import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout


# Create your views here.
def index(request):
    hsk= list_hsk.objects.all()
    return render(request, "index.html", {"list": hsk})

def hsk(request, id):
    hsk= list_hsk.objects.get(id=id)
    list1=[1,2,3]
    return render(request, "hsk.html", {"hsk": hsk, "list":list1})

def test(request, id):

    return render(request, "link.html", {"link": id})

def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user= authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else: 
            messages.info(request, "Username Or password salah")
    
    return render(request, "login.html")

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get("username")
            messages.success(request, "Akun telah dibuat untuk "+username)
            return redirect('login')
        return render(request, "register.html", {"form": form})
    return render(request, "register.html", {"form": form})

def logoutUser(request):
    logout(request)
    return redirect("login")
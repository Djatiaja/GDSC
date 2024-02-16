from django.shortcuts import render, redirect
from .models import hsk as list_hsk
from django.contrib.auth.forms import UserCreationForm
from .form import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from datetime import datetime

# Create your views here.
def index(request):
    hsk= list_hsk.objects.all()
    return render(request, "index4.html", {"list": hsk})

def hsk(request, id):
    hsk= list_hsk.objects.get(id=id)
    list1=[1,2,3]
    return render(request, "TrueHSK.html", {"hsk": hsk, "list":list1})

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
    return redirect("/")

def profile(request):
    return render(request, 'profile.html')

def roadmap(request):
    return render(request, "roadmap.html")

def detail_event(request):
    return render(request, 'detail_event.html')

def event(request):
    return render(request, 'event.html')

def uploadEvent(request):
    if request.method =='POST':
        deadline= request.POST.get('Deadline')
        Tanggal_event= request.POST.get('Tanggal-event')
        Waktu= request.POST.get('Waktu')
        instagram= request.POST.get('instagram')
        twitter= request.POST.get('twitter')
        Nama= request.POST.get('Nama')
        image= request.POST.get('image')
        benefit= request.POST.get('benefit')
        deskripsi= request.POST.get('deskripsi')
        Kumpulan =[deadline, Tanggal_event, Waktu, instagram, twitter, Nama
                   , image, benefit, deskripsi]
        if all(None is not None for kumpul in Kumpulan):
            return redirect('/')
        messages.info(request, "Mohon isi dengan benar")
    return render(request, 'uploadEvent.html')

def about(request):
    return render(request, 'about.html')

def isiHsk(request, id):
    hsk= list_hsk.objects.get(id=id)

    if request.method == "POST":
        return redirect("/"+'hsk'+"/"+str(id))
    context ={"hsk": hsk}
    return render(request, "isiHSK.html" )
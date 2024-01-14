from django.shortcuts import render
from .models import hsk as list_hsk
from django.contrib.auth.forms import UserCreationForm



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

def login(request):
    return render(request, "login.html")

def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        form.save()
        return render(request, "register.html", {"form": form})
    return render(request, "register.html", {"form": form})
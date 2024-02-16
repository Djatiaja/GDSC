import json
from django.shortcuts import render, redirect
from .models import hsk as list_hsk
from django.contrib.auth.forms import UserCreationForm
from .form import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from datetime import datetime
import pyrebase
from requests import request
from django.contrib.auth.models import User
from .models import userFirebase as userFire
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

#firebase Config

config={
  'apiKey': "AIzaSyCx_PWWt4dVxQRvcVzMe6ew8dZndSN7k1Y",
  'authDomain': "gdsc-c3246.firebaseapp.com",
  'databaseURL': "https://gdsc-c3246-default-rtdb.asia-southeast1.firebasedatabase.app",
  'projectId': "gdsc-c3246",
  'storageBucket': "gdsc-c3246.appspot.com",
  'messagingSenderId': "835610447638",
  'appId': "1:835610447638:web:0402803f5144eef102ca37",
  'measurementId': "G-S6GXNSFJ4F"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()





# Create your views here.
def index(request):
    hsk= list_hsk.objects.all()
    return render(request, "index4.html", {"list": hsk})

def hsk(request, id):
    hsk= list_hsk.objects.get(id=id)
    list1=[1,2,3]
    return render(request, "TrueHSK.html", {"hsk": hsk, "id":str(id)})

@csrf_exempt
def loginUser(request):
    if request.method == "POST":
        email = request.POST.get('Email')
        password = request.POST.get('password')
        user = auth.sign_in_with_email_and_password(email, password)
        
        token = user['idToken']
        info = auth.get_account_info(token)
        displayname = info['users'][0]['displayName']
        firebase_respon = loadDataFromFirebaseAPI(token)
        
        firebase_dict = json.loads(firebase_respon)
        print(firebase_dict)
        if 'users' in firebase_dict:
            users = firebase_dict["users"]
            if len(users)>0:
                users_one = users[0]
                if email == user["email"]:
                    if users_one["emailVerified"]== 1 or users_one["emailVerified"]==True or users_one["emailVerified"]=="True":
                        print(4)
                        proceedToLogin(email=email, username=displayname, token=token, request=request)
                        messages.info(request, 'Login Berhasil')
                        return redirect("/")
                    else:
                        messages.info(request,"Tolong verifikasi email")
                        return render(request, "login.html")
                else:
                    print(3)
                    messages.info(request,"Email User Not found")
                    return render(request, "login.html")
            else:
                messages.info(request,"User tidak ditemukan")
                print(1)
                return render(request, "login.html")
        else:
            print(2)
            messages.info('Bad Request')
    else:
        print(5)
    return render(request, "login.html")

def loadDataFromFirebaseAPI(token):

    url = "https://identitytoolkit.googleapis.com/v1/accounts:lookup"

    payload = 'key=AIzaSyCx_PWWt4dVxQRvcVzMe6ew8dZndSN7k1Y&idToken='+token
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = request("POST", url, headers=headers, data=payload)
    print(response)

    return response.text


def proceedToLogin(email, username, token, request):
    users= User.objects.filter(username=username).exists()
    if users:
        user_one = User.objects.get(username=username)
        user_one.backend = 'django.contrib.auth.backends.ModelBackend'
        kunci= userFire.objects.create(kunci=token, user=user_one)
        print(kunci)
        login(request, user_one)
        return 'Login_Success'
    else: 
        user= User.objects.create_user(email=email, username=username, password=settings.SECRET_KEY)
        user_one = User.objects.get(username=username)  
        kunci= userFire.objects.create(kunci=token, user=user_one)
        print(kunci)
        user_one.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user_one)
        return 'Login_Success'

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password1")
        user= auth.create_user_with_email_and_password(email, password)
        auth.update_profile(user['idToken'], display_name = username)
        auth.send_email_verification(user['idToken'])
        return redirect('login')

    context={
        "form": form
    }
    return render(request, 'register.html',context)

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
        nilaiListening1= request.POST.get('listening1')
        nilaiListening2= request.POST.get('listening2')
        nilaiListening3= request.POST.get('listening3')

        nilaiReading1= request.POST.get('Reading1')
        nilaiReading2= request.POST.get('Reading2')
        nilaiReading3= request.POST.get('Reading3')

        nilais= [nilaiListening1,nilaiListening2,nilaiListening3,nilaiReading1,nilaiReading2,nilaiReading3]
        
        nilais_str= ['nilaiListening1','nilaiListening2','nilaiListening3','nilaiReading1','nilaiReading2','nilaiReading3']

        for i in range(len(nilais)):
            if nilais[i] is not None:
                pass

        return redirect("/"+'hsk'+"/"+str(id))
    context ={"hsk": hsk}
    return render(request, "isiHSK.html", context )
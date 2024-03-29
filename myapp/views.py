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
from django import template
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
storage = firebase.storage()




# Create your views here.
def index(request):
    hsk= list_hsk.objects.all()
    userf=None
    notifi=0
    context={"list": hsk, "history":userf, 'notifikasi':notifi}
    data = (database.child('event').get()).val()
    dataEvent={}
    angka=1
    trueorfalse= True
    
    for event in data:
        temp=data[event]
        temp.update({"angka":angka, 'trueorfalse': trueorfalse})
        eventDict= {str(event): data[event]}
        # print(data[event])
        dataEvent.update(eventDict)
        angka+=1
        if trueorfalse:
            trueorfalse= False
        else:
            trueorfalse=True
    
    if request.user.is_authenticated:
        userf=userFire.objects.get(user=request.user)
        UID = get_UID(userf.kunci)
        user = (database.child('users').child(UID).get()).val()
        notifikasi= user['notifikasi']
        for event in notifikasi:
            if notifikasi[event]['unread']:
                notifi+=1
        context={"list": hsk, "history":userf, 'event': dataEvent, 'notifikasi':notifi}
    # print(context)
    return render(request, "index3.html", context)

def hsk(request, id):
    nilaiAsli=[]
    hsk= list_hsk.objects.get(id=id)
    userf=userFire.objects.get(user=request.user)
    userf.historyTitle = hsk.judul
    userf.historyDescribe = hsk.deskripsi
    userf.historyUrl = "hsk/"+ str(id) 
    userf.save()
    context = {"hsk": hsk, "id":str(id) }
    nilaiListen=0
    nilaiReading=0
    #mengambil data dari firebase
    info = auth.get_account_info(str(userf.kunci))
    uid = info['users'][0]['localId']
    if (database.child("users").child(uid).child('hsk').child('hsk'+str(id)).get()).val() is not None:

        nilaiAsli=(database.child("users").child(uid).child('hsk').child('hsk'+str(id)).get()).val()
        # nilaiTrue=(database.child("users").child(uid).child('hsk').get()).val()
        # for nilaiOke in nilaiTrue:
        #     nilaiOke=(database.child("users").child(uid).child(str(nilaiOke)).get()).val()
        #     for nilai in nilaiOke:
        #         # print(nilai)
        #         if "nilaiListen" in nilai:
        #             nilaiListen+=nilaiOke[nilai]
        #         elif "nilaiReading" in nilai:
        #             nilaiReading+=nilaiOke[nilai]
        # print(nilaiListen)
        # print(nilaiReading)
        print(nilaiAsli)

        context.update(nilaiAsli)
        # print(context)
    
    return render(request, "TrueHSK.html", context)

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
        # print(firebase_dict)
        print(1)
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
            messages.info(request, 'Bad Request')
    
    return render(request, "login.html")

def loadDataFromFirebaseAPI(token):

    url = "https://identitytoolkit.googleapis.com/v1/accounts:lookup"

    payload = 'key=AIzaSyCx_PWWt4dVxQRvcVzMe6ew8dZndSN7k1Y&idToken='+token
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = request("POST", url, headers=headers, data=payload)

    # print(response)
    # print('\nreponse')
    return response.text


def proceedToLogin(email, username, token, request):
    users= User.objects.filter(username=username).exists()
    if users:
        user_one = User.objects.get(username=username)
        user_one.backend = 'django.contrib.auth.backends.ModelBackend'
        kunci= userFire.objects.get(user=user_one)
        kunci.kunci = token
        kunci.save()
        login(request, user_one)
        return 'Login_Success'
    else: 
        user= User.objects.create_user(email=email, username=username, password=settings.SECRET_KEY)
        user_one = User.objects.get(username=username)  
        kunci= userFire.objects.create(kunci=token, user=user_one)
        # print(kunci)
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
        UID=get_UID(user['idToken'])
        auth.send_email_verification(user['idToken'])
        messages.info(request,"Email Verifikasi telah dikirim")
        data={
            'totalNilai': 0
        }
        database.child('users').child(UID).set(data)
        return redirect('login')

    context={
        "form": form
    }
    return render(request, 'register.html',context)

def logoutUser(request):
    logout(request)
    return redirect("/")

def profile(request):
    # isiUser()

    userf=userFire.objects.get(user=request.user)
    listen=0
    reading=0
    nilaiListen=0
    nilaiReading=0
    nilaiTotal=0
    angka =0
    #mengambil data dari firebase
    info = auth.get_account_info(str(userf.kunci))
    uid = info['users'][0]['localId']
    if (database.child("users").child(uid).get()).val() is not None:
        user= (database.child('users').child(uid).get()).val()
        nilaiTotal=(user['totalNilai'])
        nilaiListen= user['nilaiListen']
        nilaiReading = user['nilaiReading']

        users= (database.child('users').get()).val()

        listNilaiUser=[]
        for user in users:
            # print(users[str(users)])
            temp= users[user]['totalNilai']
            listNilaiUser.append(temp)
        
        listNilaiUser.sort(reverse=True)
        angka = listNilaiUser.index(nilaiTotal)
        angka +=1
        placment= str(angka)[-1]
        print(placment)

    context={
        "barListen":((nilaiListen*90)/100),
        "barReading": (nilaiReading*90)/100,
        'nilaiListen': int(nilaiListen),
        'nilaiReading': int(nilaiReading),
        "skor": nilaiTotal,
        "history": userf,
        "rangking": angka,
        "placement": int(placment)
    }
    return render(request, 'profile.html', context)

def roadmap(request):
    return render(request, "roadmap.html")

def detail_event(request, id):
    data= (database.child('event').child(str(id)).get()).val()
    context={}
    context.update(data)
    # print(context)
    return render(request, 'detail_event2.html', context)

def event(request):
    data = (database.child('event').get()).val()
    dataEvent={}
    angka=1
    trueorfalse= True
    for event in data:
        temp=data[event]
        temp.update({"angka":angka, 'trueorfalse': trueorfalse})
        eventDict= {str(event): data[event]}
        # print(data[event])
        dataEvent.update(eventDict)
        angka+=1
        if trueorfalse:
            trueorfalse= False
        else:
            trueorfalse=True
    context={'event':dataEvent}
    
    # print(context)
    return render(request, 'event.html', context)

def uploadEvent(request):
    if request.method =='POST':
        imageName = None
        author = str(request.user)
        time = str(datetime.now())
        time =time[:19]
        deadline= request.POST.get('Deadline')
        Tanggal_event= request.POST.get('Tanggal-event')
        Waktu= request.POST.get('Waktu')
        instagram= request.POST.get('instagram')
        twitter= request.POST.get('twitter')
        Nama= request.POST.get('Nama')
        benefit= request.POST.get('benefit')
        deskripsi= request.POST.get('deskripsi')
        kategori= request.POST.get('kategori')
        urls= request.POST.get('urls')
        try:
            image= request.FILES['image']
            imageName= str(request.FILES['image'].name)
        except:
            imageName=None
        # print(imageName)
        KumpulanCheck =[deadline, Tanggal_event, Waktu, instagram, twitter, Nama, imageName, benefit, deskripsi, kategori, author, time, urls]
        Kumpulan={'deadline': deadline, 
                  'Tanggal_event': Tanggal_event,
                  'Waktu': Waktu,
                  'instagram': instagram,
                  "Nama": Nama,
                  'image': imageName,
                  'benefit': benefit,
                  'deskripsi': deskripsi,
                  'kategori': kategori,
                  'author': author,
                  "timeUpload": time}
        
        # print(KumpulanCheck)
        if all(kumpul != '' for kumpul in KumpulanCheck):
            storage.child('event/'+imageName).put(image)
            image= storage.child('event/'+imageName).get_url(image)
            Kumpulan={'deadline': deadline, 
                  'Tanggal_event': Tanggal_event,
                  'Waktu': Waktu,
                  'instagram': instagram,
                  'twitter':twitter,
                  "Nama": Nama,
                  'image': image,
                  'benefit': benefit,
                  'deskripsi': deskripsi,
                  'kategori': kategori,
                  'author': author,
                  "timeUpload": time,
                  'urls': urls}
            
            data={'NamaEvent': Nama, 'unread':True}
            database.child("event").child(str(Nama)).set(Kumpulan)
            users = (database.child('users').get()).val()
            for user in users:
                database.child('users').child(user).child('notifikasi').child(Nama).set(data)

            messages.info(request, "Upload Berhasil")
            return redirect('/')
        else:
            messages.info(request, "Mohon isi dengan benar")
    return render(request, 'uploadEvent.html')

def about(request):
    gambar = (database.child('event').child("Webinar").child('asdw').child('image').get()).val()
    # print(gambar)
    return render(request, 'about.html', )

def isiHsk(request, id):
    hsk= list_hsk.objects.get(id=id)
    if request.user.is_authenticated:
        userf=userFire.objects.get(user=request.user)
        info = auth.get_account_info(str(userf.kunci))
        uid = info['users'][0]['localId']
        
    context ={"hsk": hsk}
    # if database.child("users").child(uid).child("hsk"+str(id)).get() != None:
    #     data = (database.child("users").child(uid).child("hsk"+str(id)).get()).val()
    #     context.update(data)

    nilaiListen=0
    nilaiReading=0
    listen=0
    reading=0

    if request.method == "POST":
        nilaiListening1= request.POST.get('listening1')
        nilaiListening2= request.POST.get('listening2')
        nilaiListening3= request.POST.get('listening3')

        nilaiReading1= request.POST.get('Reading1')
        nilaiReading2= request.POST.get('Reading2')
        nilaiReading3= request.POST.get('Reading3')

        nilais=[nilaiListening1, nilaiListening2, nilaiListening3, nilaiReading1,nilaiReading2,nilaiReading3]
        for i in range( len(nilais)):
            # print(nilais[i])
            if nilais[i] == '':
                nilais[i]=0
        
        dict= {"nilaiListening1":int(nilais[0]),"nilaiListening2":int(nilais[1]),"nilaiListening3":int(nilais[2]),
                 "nilaiReading1":int(nilais[3]),"nilaiReading2":int(nilais[4]),"nilaiReading3":int(nilais[5])}        
        
        userf=userFire.objects.get(user=request.user)
        
        info = auth.get_account_info(str(userf.kunci))
        uid = info['users'][0]['localId']
        
        database.child("users").child(uid).child('hsk').child("hsk"+str(id)).set(dict)
        nilaiTrue=(database.child("users").child(uid).child('hsk').get()).val()
        # for event in nilaiTrue:
        #     if event != 
        # print(coba)
        for nilaiOke in nilaiTrue:
            nilaiOke=(database.child("users").child(uid).child('hsk').child(str(nilaiOke)).get()).val()
            for nilai in nilaiOke:
                # print(nilai)
                if "nilaiListen" in nilai:
                    if nilaiOke[nilai] > 0:
                        nilaiListen+=nilaiOke[nilai]
                        listen+=1
                elif "nilaiReading" in nilai:
                    if nilaiOke[nilai] > 0:
                        nilaiReading+=nilaiOke[nilai]
                        reading+=1
        

        nilaiTotal= nilaiListen+nilaiReading
        if listen>0:
            nilaiListen/=listen
        if reading>0:
            nilaiReading/=listen

        database.child('users').child(uid).update({'totalNilai':nilaiTotal, 'nilaiReading': nilaiReading, 'nilaiListen':nilaiListen})


        return redirect("/"+'hsk'+"/"+str(id))
    return render(request, "isiHSK.html", context )


def isiUser():
    users = (database.child('users').get()).val()
    for user in users:
        print(user)
        database.child('users').child(user).child("total_nilai").set({'NilaiTotal': 0})


def get_UID(token):
    user = auth.get_account_info(token)
    UID = user['users'][0]['localId']
    return UID


def partition(array, low, high):
  pivot = array[high]
  i = low - 1
  for j in range(low, high):
    if array[j] <= pivot:
      i = i + 1
      (array[i], array[j]) = (array[j], array[i])
  (array[i + 1], array[high]) = (array[high], array[i + 1])
  return i + 1

def quickSort(array, low, high):
  if low < high:
    pi = partition(array, low, high)
    quickSort(array, low, pi - 1)
    quickSort(array, pi + 1, high)


def notif(request):
    userf=userFire.objects.get(user=request.user)
    UID  = get_UID(userf.kunci)
    notifikasi = (database.child('users').child(UID).child('notifikasi').get()).val()
    context={}
    temp={}
    for notif in notifikasi:
        tempo= (database.child('event').child(notif).get()).val()
        print(tempo)
        temp.update({str(notif): tempo})
        database.child('users').child(UID).child('notifikasi').child(notif).update({"unread":False})
    context={
        'event': temp
    }
    print(context)
    return render(request, 'notif.html', context)
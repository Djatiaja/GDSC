from django.urls import path
from . import views


urlpatterns=[
    path("", views.index , name="index"),
    path("hsk/<str:id>", views.hsk, name="hsk"),
    path("isiHsk/<str:id>", views.isiHsk, name="isiHsk"),
    path('login', views.loginUser, name="login"),
    path('register', views.register, name="register"),
    path("logout", views.logoutUser, name="logout"),
    path('profile', views.profile, name="profile"),
    path("roadmap", views.roadmap, name="roadmap"),
    path('detail_event/<str:id>', views.detail_event, name='detail_event'),
    path('event', views.event, name="event"),
    path("upload", views.uploadEvent, name='uploadEvent'),
    path('about', views.about, name="about")

]

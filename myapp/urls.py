from django.urls import path
from . import views


urlpatterns=[
    path("", views.index , name="index"),
    path("hsk/<str:id>", views.hsk, name="hsk"),
    path("test/<str:id>", views.test, name="test")
]
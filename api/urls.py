from django.urls import path

from .views import GetList, InsertList, Register

app_name = 'api'

urlpatterns = [
    path('register/', Register.as_view()),
    path('list/add/', InsertList.as_view()),
    path('list/get/', GetList.as_view()),
    path('list/update/', GetList.as_view()),
]

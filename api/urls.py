from django.urls import path

from .views import Register, Tasks, loadjson

app_name = 'api'

urlpatterns = [
    path('register/', Register.as_view()),
    path('task/add/', Tasks.as_view()),
    path('task/get/', Tasks.as_view()),
    path('task/update/', Tasks.as_view()),
    path('task/delete/', Tasks.as_view()),
    path('schema-swagger/', loadjson),
]

from django.urls import path

from .views import Register, Tasks, loadjson

app_name = 'api'

urlpatterns = [
    path('register/', Register.as_view()),
    path('task/', Tasks.as_view()),
    path('task/<int:id>', Tasks.as_view()),
    path('task/add/', Tasks.as_view()),
    path('task/update/', Tasks.as_view()),
    path('task/delete/<int:id>/', Tasks.as_view()),
    path('schema-swagger/', loadjson),
]

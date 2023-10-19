from django.urls import path

from .views import Login, Register, Tasks, loadjson

app_name = 'api'

urlpatterns = [
    # User
    path('login/', Login.as_view()),
    path('register/', Register.as_view()),

    # Tasks
    path('task/', Tasks.as_view()),
    path('task/<int:id>', Tasks.as_view()),
    path('task/add/', Tasks.as_view()),
    path('task/update/', Tasks.as_view()),
    path('task/delete/<int:id>/', Tasks.as_view()),

    # Swagger json endpoit
    path('schema-swagger/', loadjson),
]

from django.urls import path
from . import views

urlpatterns = [
    path('greet/', views.say_hello, name='greet'),
    path('signup/', views.sign_up, name='signup'),
    path('login', views.login, name="login"),
]

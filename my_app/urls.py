from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('New_Search', views.New_Search, name = 'New_Search')
]
from django.urls import path
from . import views

app_name = 'wcss'

urlpatterns = [
    path('', views.index, name='index'),
    path('indextest', views.indextest, name='indextest'),
]

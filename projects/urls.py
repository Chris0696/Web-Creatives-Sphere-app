from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.projects, name='projects'),

    path('project/<str:pk>/', views.project, name='project'),
    path('create-project/', views.createProject, name='create-project'),
    path('edit-project/<str:pk>/', views.updateProject, name='edit-project'),
    path('delete-project/<str:pk>/', views.deleteProject, name='delete-project'),
]

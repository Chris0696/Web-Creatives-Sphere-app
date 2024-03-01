from django.urls import path
from .views import authors, users, customers


app_name = 'users'

urlpatterns = [
    path('login/', users.loginUser, name='login'),
    path('logout/', users.logoutUser, name='logout'),

    path('authors/', users.AuthorsProfiles, name="profiles"),
    path('author/profile/<str:pk>/', users.AuthorProfile, name="author-profile"),

    path('customer/', users.CustomersProfiles, name="customerprofiles"),
    path('customer/profile/<str:pk>/', users.customerProfile, name="customer-profile"),



    path('create-skill/', authors.createSkill, name="create-skill"),
    path('update-skill/<str:pk>/', authors.updateSkill, name="update-skill"),
    path('delete-skill/<str:pk>/', authors.deleteSkill, name="delete-skill"),

    # path('inbox/', users.inbox, name="inbox"),
    # path('message/<str:pk>/', users.viewMessage, name="message"),
    # path('send-message/<str:pk>/', users.SendMessage.as_view(), name='send-message'),
    # path('send-message/<str:pk>/', users.sendMessage, name="send-message"),




    # path('register/', views.registerUser, name='register'),

]



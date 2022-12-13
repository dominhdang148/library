from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('', views.home, name="home"),
    path('document/<str:pk>/', views.document, name='document'),
    path('profile/<str:pk>/', views.userProfile, name='profile'),
    path('create-document/', views.createDocument, name='create-document'),
    path('update-document/<str:pk>/',
         views.updateDocument, name='update-document'),
    path('delete-document/<str:pk>/',
         views.deleteDocument, name='delete-document'),
    path('delete-comment/<str:pk>/',
         views.deleteComment, name='delete-comment'),

]

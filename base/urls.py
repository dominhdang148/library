from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('document/<str:pk>/', views.document, name='document')
]

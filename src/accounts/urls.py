from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

app_name = 'accounts'
urlpatterns = [
    path('', auth_view.LoginView.as_view(), name='login'),
    path('register/', views.signup, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

]


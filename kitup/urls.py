from django.urls import path
from django.conf.urls import url

# Access the views for the kitup web application.
from kitup import views

# Enable the use of template tags by defining the app name.
app_name = 'kitup'

# Parameter for path function is the string to match;
# Empty means that a match will be made when nothing is there;
# Second parameter denotes the view that's to be called;
# Third parameter, name, is an optional parameter;
# Provides a concenient way to reference the view;
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
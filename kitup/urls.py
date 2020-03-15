from django.urls import path
from django.conf.urls import url

# Access the views for the kitup web application.
from kitup import views

# Enable the use of template tags by defining the app name.
app_name = 'kitup'

# Parameter for path function is the string to match;
# Empty means that a match will be made when nothing is there;
# Second parameter denotes the view that's to be called;
# The third parameter, name, is an optional parameter;
# Provides a convenient way to reference the view;
urlpatterns = [
    path('', views.index, name='index'),
    
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('recover/', views.user_recover, name='recover'),
    path('profile/', views.user_profile, name='profile'),
    path('settings/', views.user_settings, name='settings'),

    path('match/create', views.match_create, name='match_create'),
    path('match/leave/<int:match_id>/', views.match_leave, name='match_leave'),
    path('match/find/<int:match_id>/', views.match_find, name='match_find'),
    path('match/view/<int:match_id>/', views.match_view, name='match_view'),
    path('match/post/<int:match_id>/', views.match_post, name='match_post'),
]
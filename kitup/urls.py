from django.urls import path
from django.conf.urls import url

# The views thats are to be displayed depending on the URL.
from kitup import views

# Enable the use of template tags by defining the app name.
app_name = 'kitup'

'''
The parameter for the path function is the string to match, where empty
implies that a match will be made when nothing is there i.e. empty string.

The second parameter denotes the view that's to be called.

The third parameter - the name / tag - is an optional parameter. It 
proviees a convenient way to reference the view - opposed to using
the URL.
'''
urlpatterns = [
    path('', views.index, name='index'),
    
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),

    path('password-reset/', views.password_reset, name='password_reset'),
    path('password-reset/done/', views.password_reset_done, name='password_reset_done'),
    #path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView, name='password_reset_confirm'),
    #path('reset/done/', views.PasswordResetCompleteView, name='password_reset_complete'),

    path('profile/', views.user_profile, name='user_profile'),
    path('profile/<int:user_id>/', views.user_view_profile, name='user_view_profile'),
    path('settings/', views.user_settings, name='user_settings'),
    path('report/<int:reported_user_id>', views.user_report, name='user_report'),

    path('match/create', views.match_create, name='match_create'),
    path('match/leave/<int:match_id>/', views.match_leave, name='match_leave'),
    path('match/view/<int:match_id>/', views.match_view, name='match_view'),
    path('match/rate/<int:match_id>/', views.match_rate, name='match_rate'),
]
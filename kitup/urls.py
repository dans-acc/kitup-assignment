from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views

# The views thats are to be displayed depending on the URL.
from kitup import views as kitup_views

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
    path('', kitup_views.index, name='index'),
    
    path('register/', kitup_views.user_register, name='user_register'),
    path('web_response/', kitup_views.web_response, name='web_response'),
    path('login/', kitup_views.user_login, name='user_login'),
    path('logout/', kitup_views.user_logout, name='user_logout'),

    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('profile/', kitup_views.user_profile, name='user_profile'),
    path('profile/<int:profile_id>/', kitup_views.user_view_profile, name='user_view_profile'),
    path('settings/', kitup_views.user_settings, name='user_settings'),

    path('match/create', kitup_views.match_create, name='match_create'),
    path('match/edit/<int:match_id>', kitup_views.match_edit, name='match_edit'),
    path('match/join/<int:match_id>', kitup_views.match_join, name='match_join'),
    path('match/leave/<int:match_id>/', kitup_views.match_leave, name='match_leave'),
    path('match/report/<int:participant_id>/', kitup_views.match_report, name='match_report'),
    path('match/accept/<int:participant_id>/', kitup_views.match_accept, name='match_accept'),
    path('match/kick/<int:participant_id>/', kitup_views.match_kick, name='match_kick'),
    path('match/rate/<int:participant_id>/', kitup_views.match_rate, name='match_rate'),
    path('match/view/<int:match_id>/', kitup_views.match_view, name='match_view'),
]
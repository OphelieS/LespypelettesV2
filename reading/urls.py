import django 

from reading import views

from django.urls import path
from reading.views import game, get_random_word, update_stars, detect_emotion
from reading.views import signup, signup_done, signin, signin_done,  CustomLoginView

app_name = 'reading'
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('templates/compte/', views.compte, name='compte'),
    path('login/', CustomLoginView.as_view(), name='account_login'),
    path('logout/', views.logout, name='logout'),
    path('accounts/signup/', views.signup, name='signup'),
    path('signup_done/', views.signup_done, name='signup_done'),
    path('signin/', views.signin, name='signin'),
    path('signin_done/', views.signin_done, name='signin_done'),
    path('detect_emotion/', views.detect_emotion, name='detect_emotion'),
    path('update_stars/', views.update_stars, name='update_stars'),
    path('game/', views.game, name='game'),
    path('random-word/', get_random_word, name='get_random_word'),

    path('user_profile/', views.user_profile, name='user_profile'),
]

from django.urls import path

from .views import SignUpView, explorePage, getUserDetails


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/',getUserDetails,name='profile'),
    path('explore/',explorePage,name='explore')
]
from django.urls import path

from .views import LoginPageView, LogoutView, SignUpView

urlpatterns = [
    path('signup', SignUpView.as_view(), name='signup'),
    path('', LoginPageView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout')
]
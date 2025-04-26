from django.urls import path
from ..views.register import AuthUserView, LoginView, LogoutView

urlpatterns = [
    path('register/', AuthUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]
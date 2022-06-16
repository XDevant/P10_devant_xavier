from django.urls import path
from .views import LoginView, SignupView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='login_refresh'),
    path('signup/', SignupView.as_view(), name='signup'),
]

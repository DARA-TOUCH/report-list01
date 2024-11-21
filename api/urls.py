from django.urls import path
from .views import CreateUserView, LoginTemplateView, HomePageView, test
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'api'

urlpatterns = [
    path('user/register/', CreateUserView.as_view(), name='user-register'),
    path('user/login/', LoginTemplateView.as_view(), name='login-template'),
    
    path('token/', TokenObtainPairView.as_view(), name='user-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('home/', HomePageView.as_view(), name='home'),
    path('test/', test, name='test'),
    
]

from django.urls import path
from users.views import CustomTokenObtainPairView, GetUserStatusView,LoginView
#from rest_framework_simplejwt.views import TokenObtainPairView
#from django.contrib.auth.views import LoginView as DjangoLoginView
from .views import GetUserStatusView





urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/', LoginView.as_view(), name='login'),
    path('user-status/', GetUserStatusView.as_view(), name='user-status'),
    #path('csrf/', YourCSRFView.as_view(), name='get_csrf'),
]

from django.contrib.auth import authenticate,login
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
import logging
from django.views.decorators.csrf import get_token
from django.middleware.csrf import get_token as get_csrf_token

from rest_framework_simplejwt.views import TokenObtainPairView

logger = logging.getLogger(__name__)

def generateTokens(user_param):
    print(user_param)
    if True:
        #  user = User.objects.get(username=user.username)
        #  refresh = RefreshToken.for_user(user)
         #response.data['refresh'] = str(refresh)
         #response.data['access'] = str(refresh.access_token)
        return {}   
    else:
        return{}
        
    


class CustomTokenObtainPairView(TokenObtainPairView):
    @csrf_exempt
    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            if response.status_code == 200:
                username = request.data.get('username')
                if username:
                    user = User.objects.get(username=username)
                    refresh = RefreshToken.for_user(user)
                    response.data['refresh'] = str(refresh)
                    response.data['access'] = str(refresh.access_token)
            return response
        except User.DoesNotExist:
            logger.error("Error in CustomTokenObtainPairView: User not found")
            return JsonResponse({'error': 'Credenciais inválidas'}, status=401)
        except Exception as e:
            logger.error(f"Error in CustomTokenObtainPairView: {str(e)}")
            return JsonResponse({'error': 'Erro ao tentar fazer login'}, status=500)

class LoginView(View):
    @csrf_exempt
    def post(self, request):
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                logger.info(f"Usuário {username} fez login com sucesso.")
                user_c = User.objects.get(username=username)
                refresh = RefreshToken.for_user(user_c)
                tokens = {"refreshToken": str(refresh), "accessToken": str(refresh.access_token)}
                print(tokens)
                return JsonResponse({'message': 'Login bem-sucedido', 'user_id': user.id, "tokens": tokens})
            else:
                logger.warning(f"Tentativa de login falhou para o usuário {username}.")
                return JsonResponse({'error': 'Credenciais inválidas. Verifique seu nome de usuário e senha.'}, status=401)

        except Exception as e:
            logger.error(f"Error in LoginView: {str(e)}")
            return JsonResponse({'error': 'Erro ao tentar fazer login'}, status=500)
        




class GetUserStatusView(View):
    def post(self, request):
        print("UYoo=")
        if request.POST.get('is_authenticated') == "true":
            #request.POST.get('is_authenticated')
            return JsonResponse({'authenticated': True, 'username': request.user.username, 'user_id': request.user.id})
        else:
            return JsonResponse({'authenticated': False, 'username': None, 'user_id': None})
from functools import wraps
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status


class PasswordHasher:
    @staticmethod
    def hash_password(password: str) -> str:
        return make_password(password)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return check_password(password, hashed_password)


class JWTManager:
    @staticmethod
    def create_access_token(user):
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        access['user_id'] = user.id
        access['email'] = user.email
        access['name'] = user.first_name

        return {
            'access_token': str(access),
            'refresh_token': str(refresh),
        }


def create_access_token(user):
    return JWTManager.create_access_token(user)


def get_jwt_identity(request):
    user = getattr(request, 'user', None)
    if user and user.is_authenticated:
        return user.id
    return None


def jwt_required(view_func):
    @wraps(view_func)
    def wrapped(view, request, *args, **kwargs):
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return Response(
                {'message': 'Authentication credentials were not provided or are invalid.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return view_func(view, request, *args, **kwargs)
    return wrapped

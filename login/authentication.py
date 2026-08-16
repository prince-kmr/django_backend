import os
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import authentication, exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication as SimpleJWTAuthentication


class JWTAuthentication(SimpleJWTAuthentication):
    pass


if not firebase_admin._apps:
    firebase_path = getattr(settings, 'FIREBASE_SERVICE_ACCOUNT_PATH', '')
    if firebase_path:
        cred = credentials.Certificate(firebase_path)
        firebase_admin.initialize_app(cred)


class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header:
            return None

        parts = auth_header.split()

        if len(parts) != 2:
            return None

        prefix, token = parts

        if prefix.lower() != 'firebase':
            return None

        try:
            decoded_token = firebase_auth.verify_id_token(token)
            firebase_uid = decoded_token.get('uid')
            email = decoded_token.get('email')
            name = decoded_token.get('name', '')
            email_verified = decoded_token.get('email_verified', False)

            if not email:
                raise exceptions.AuthenticationFailed('Firebase token missing email.')

            if not email_verified:
                raise exceptions.AuthenticationFailed('Email is not verified with Firebase.')

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email,
                    'first_name': name or '',
                }
            )

            if created and not user.username:
                user.username = email
                user.save()

            request.firebase_uid = firebase_uid
            request.firebase_decoded_token = decoded_token

            return (user, token)

        except Exception as e:
            raise exceptions.AuthenticationFailed(f'Firebase authentication failed: {str(e)}')

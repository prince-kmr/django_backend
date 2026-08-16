from django.contrib.auth.models import User
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer
from .utils.auth_utils import create_access_token, get_jwt_identity
from firebase_admin import auth as firebase_auth


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        tokens = create_access_token(user)

        return Response({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'name': user.first_name,
                'email': user.email,
            },
            'tokens': tokens
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email', '').strip().lower()
        password = request.data.get('password', '')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'message': 'Invalid email or password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.check_password(password):
            return Response(
                {'message': 'Invalid email or password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        tokens = create_access_token(user)

        return Response({
            'message': 'Login successful',
            'user': {
                'id': user.pk,
                'name': user.first_name,
                'email': user.email
            },
            'tokens': tokens
        }, status=status.HTTP_200_OK)


class FirebaseGoogleLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        id_token = request.data.get('id_token')

        if not id_token:
            return Response(
                {'message': 'id_token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
            firebase_uid = decoded_token.get('uid')
            email = decoded_token.get('email')
            name = decoded_token.get('name', '')
            email_verified = decoded_token.get('email_verified', False)

            if not email:
                return Response(
                    {'message': 'Firebase token does not contain an email'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not email_verified:
                return Response(
                    {'message': 'Firebase email is not verified'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email,
                    'first_name': name or '',
                }
            )

            if not user.first_name and name:
                user.first_name = name
                user.save(update_fields=['first_name'])

            tokens = create_access_token(user)

            return Response({
                'message': 'Firebase login successful',
                'firebase_uid': firebase_uid,
                'is_new_user': created,
                'user': {
                    'id': user.id,
                    'name': user.first_name,
                    'email': user.email,
                },
                'tokens': tokens
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'message': f'Invalid Firebase token: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({
            'user_id': get_jwt_identity(request),
            'name': request.user.first_name,
            'email': request.user.email,
        })

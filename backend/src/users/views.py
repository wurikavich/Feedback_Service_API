from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from src.base.permissions import AllowAdminOnly
from src.users.models import User
from src.users.serializers import AuthSignupSerializer, UsersSerializer
from src.users.utils import send_confirmation_code


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Регистрация нового пользователя по username и email."""
    serializer = AuthSignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    user, _ = User.objects.get_or_create(username=username, email=email)
    return send_confirmation_code(request, user, email)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_token(request):
    """Получение JWT-токена по username и confirmation code."""
    user = get_object_or_404(User, username=request.data.get('username'))
    confirmation_code = request.data.get('confirmation_code')
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response({'error': 'Неверный username или код подтверждения!'},
                    status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    """CRUD пользователей."""
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (AllowAdminOnly,)
    lookup_field = 'username'

    @action(methods=['GET', 'PATCH'],
            detail=False,
            permission_classes=(IsAuthenticated,),
            url_path='me')
    def get_patch_profile(self, request):
        """Получение/Изменение данных учетной записи пользователя."""
        if request.method == 'PATCH':
            serializer = UsersSerializer(
                request.user,
                data=request.data,
                partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UsersSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

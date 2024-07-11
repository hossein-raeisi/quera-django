from rest_framework.authentication import BaseAuthentication, TokenAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission

from Quera.drf.models import User, UserToken


class SimpleAuthentication(BaseAuthentication):
    """
    All authentication classes should extend BaseAuthentication.
    """

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if auth[1] == 'secret':
            return User.objects.get(code=1), 'secret'

    def authenticate_header(self, request):
        return 'Token'


class SimpleAuthentication2(BaseAuthentication):
    """
    All authentication classes should extend BaseAuthentication.
    """

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if auth[1] == b'secret2':
            return User.objects.get(code=2), 'secret2'

    def authenticate_header(self, request):
        return 'Token'


class UserTokenAuthentication(TokenAuthentication):
    model = UserToken

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed()

        return (token.user, token)


class HasHighAuthorizationLevel(BasePermission):
    def has_permission(self, request, view):
        return request.user.authorization_level >= 4


class HasRightName(BasePermission):
    def has_permission(self, request, view):
        return request.user.name == 'hossein-1'

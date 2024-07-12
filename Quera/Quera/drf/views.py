from http import HTTPMethod

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action, api_view
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import CursorPagination, LimitOffsetPagination, PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.throttling import SimpleRateThrottle
from rest_framework.views import APIView

from .models import Book
from .serializers import BookSerializer, RestrictedBookSerializer, UserSerializer, UsersSerializer
from .services import HasHighAuthorizationLevel, HasRightName, UserTokenAuthentication


# Views

# https://www.django-rest-framework.org/api-guide/views/#dispatch-methods

class MyAPIView(APIView):
    def get(self, request: Request) -> Response:
        serializer = UsersSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        return Response(data.name, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = UsersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        return Response(data.names, status=status.HTTP_200_OK)


@api_view(['GET'])
def my_api_view(request: Request) -> Response:
    if request.method == 'GET':
        ...
    return Response('hello')


class UserAPI(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(user.name)


# authentication and authorization
class UserAPIProtected(APIView):
    authentication_classes = [UserTokenAuthentication]
    # https://www.django-rest-framework.org/api-guide/authentication/
    permission_classes = [HasHighAuthorizationLevel & HasRightName]

    # https://www.django-rest-framework.org/api-guide/permissions/

    # throttle_classes = [SimpleRateThrottle, ]  # https://www.django-rest-framework.org/api-guide/throttling/

    def get(self, request: Request) -> Response:
        return Response(request.user.name)


class CleanerUserAPIProtected(APIView):
    def get_authenticators(self):
        return super().get_authenticators() + [UserTokenAuthentication]

    def get_permissions(self):
        return super().get_permissions() + [HasHighAuthorizationLevel & HasRightName]

    # throttle_classes = [SimpleRateThrottle, ]  # https://www.django-rest-framework.org/api-guide/throttling/

    def get(self, request: Request) -> Response:
        return Response(request.user.name)


class SimpleAPI(APIView):

    def get(self, request: Request) -> Response:
        return Response('accepted')


class CleanerProtectedAPIView(APIView):

    def get_authenticators(self):
        return super().get_authenticators() + [TokenAuthentication]

    def get_permissions(self):
        return super().get_permissions() + [IsAuthenticated]

    def get_throttles(self):
        return super().get_throttles() + [SimpleRateThrottle]

    def post(self, request: Request) -> Response:
        pass  # todo


# Generic Views
# https://www.django-rest-framework.org/api-guide/generic-views/

class BookGenericView(generics.ListCreateAPIView):
    def get_authenticators(self):
        return [UserTokenAuthentication]

    def get_permissions(self):
        return super().get_permissions() + [IsAuthenticated]

    def get_queryset(self):
        if ...:
            return Book.objects.all()
        return Book.objects.filter(...)

    def get_serializer_class(self):
        if self.request.user.authorization_level >= 3:
            return BookSerializer
        return RestrictedBookSerializer

    # we can override the default implementations
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)  # todo


class BookGenericRetrieve(generics.RetrieveAPIView):
    def get_queryset(self):
        return Book.objects.all()  # todo : more advanced logic

    def get_serializer_class(self):
        return BookSerializer  # todo: more advanced logic


# we can implement our own mixins
class MyMixin:
    pass  # todo


# ViewSets
# https://www.django-rest-framework.org/api-guide/viewsets/
# combine the logic for a set of related views in a single class

class BookViewSet(viewsets.ViewSet):
    queryset = Book.objects.all()

    def list(self, request: Request) -> Response:
        serializer = BookSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request: Request, pk) -> Response:
        book = get_object_or_404(self.queryset, pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    # custom actions
    @action(detail=False, methods=[HTTPMethod.GET], url_name='detailed-action')
    def count(self, request: Request) -> Response:
        return Response({'objects_count': self.queryset.count()})

    @action(detail=True, methods=['POST'])
    def general_action(self, request: Request, pk: int = None) -> Response:
        book = get_object_or_404(self.queryset, pk=pk)
        author_other_books = self.queryset.filter(author=book.author)
        serializer = BookSerializer(author_other_books, many=True)
        return Response(serializer.data)


class BookModelViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return Book.objects.all()

    def get_serializer_class(self):
        return BookSerializer


class BookReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):

    def get_queryset(self):
        return Book.objects.all()

    def get_serializer_class(self):
        return BookSerializer


# CORS
# https://github.com/adamchainz/django-cors-headers

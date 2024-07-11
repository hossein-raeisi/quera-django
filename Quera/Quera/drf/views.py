import dataclasses
from typing import Any

from rest_framework import generics, mixins, serializers, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.throttling import SimpleRateThrottle
from rest_framework.views import APIView

from Quera.drf.models import User
from .services import HasHighAuthorizationLevel, HasRightName, UserTokenAuthentication


# Views

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


# https://www.django-rest-framework.org/api-guide/views/#dispatch-methods


# serialization and validation
# https://www.django-rest-framework.org/api-guide/serializers/
# https://www.django-rest-framework.org/api-guide/validators/


@dataclasses.dataclass
class AddressData:
    city: str


@dataclasses.dataclass
class UserData:
    names: list[str]
    address: AddressData


class Address(serializers.Serializer):
    city = serializers.CharField(max_length=20)


class UsersSerializer(serializers.Serializer):
    names = serializers.ListSerializer(child=serializers.CharField(max_length=20), max_length=2, min_length=1)
    address = Address()

    def create(self, validated_data: dict[Any, Any]) -> Any:
        return UserData(
            names=validated_data.get('names'),
            address=AddressData(city=validated_data['address']['city']),
        )

    def update(self, instance: Any, validated_data: dict[Any, Any]) -> Any:
        return self.save(**validated_data | dataclasses.asdict(instance))  # todo

    def validate(self, data: dict) -> dict:
        if len(data['names']) > 1 and data['address']['city'] == 'tehran':
            raise ValidationError({'error': ['bad number and city']})

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


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


# middlewares

# ViewSets
# https://www.django-rest-framework.org/api-guide/viewsets/
# combine the logic for a set of related views in a single class

class MyViewSet(viewsets.ModelViewSet):
    # queryset = MyModel.objects.all()

    @action(detail=True, methods=['GET'])
    def my_action(self, request: Request, pk: Any = None) -> Response:
        pass  # todo

    # todo: reversing


# Generic Views
# https://www.django-rest-framework.org/api-guide/generic-views/

class MyGenericViewSet(generics.ListAPIView, mixins.UpdateModelMixin):

    def get_queryset(self):
        pass
        # return MyModel.objects.all()


class MyMixin:
    pass  # todo

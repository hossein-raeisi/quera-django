import dataclasses
from typing import Any

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Book, User


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


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class RestrictedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['name']

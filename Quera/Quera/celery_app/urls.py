from django.urls import path

from .views import get_square

urlpatterns = [
    path('square/', get_square, name='square'),
]

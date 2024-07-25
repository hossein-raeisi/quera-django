from django.urls import path

from Quera.async_app.views import GetAnimal, create_animal, get_animal, google_animal

urlpatterns = [
    path('create-animal/', create_animal, name='create-animal'),
    path('get-animal/', get_animal, name='get-animal'),
    path('animal/', GetAnimal.as_view(), name='animal'),
    path('animal/google/', google_animal, name='google-animal'),
]

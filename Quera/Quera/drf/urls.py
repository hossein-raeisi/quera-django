from django.urls import path
from rest_framework.routers import DefaultRouter

from Quera.drf.views import MyAPIView, MyViewSet, UserAPI, UserAPIProtected, my_api_view

urlpatterns = [
    path('my-api-view/', MyAPIView.as_view(), name='my-api-view'),
    path('my-api-view-2/', my_api_view, name='my-api-view-2'),
    path('user/', UserAPI.as_view(), name='user'),
    path('user-protected/', UserAPIProtected.as_view(), name='user-protected'),
]

router = DefaultRouter()
router.register(r'view-set', MyViewSet, basename='view-set')
urlpatterns += router.urls

# path('users/', ListCreateAPIView.as_view(queryset=User.objects.all(), serializer_class=UserSerializer), name='user-list')

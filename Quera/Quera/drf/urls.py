from django.urls import path
from rest_framework.routers import DefaultRouter

from Quera.drf.views import (
    BookCachedAPI, BookGenericRetrieve, BookGenericView, BookModelViewSet, BookPaginatedReadOnlyModelViewSet,
    BookViewSet, MyAPIView,
    SimpleAPI, UserAPI,
    UserAPIProtected, my_api_view
)

urlpatterns = [
    path('my-api-view/', MyAPIView.as_view(), name='my-api-view'),
    path('my-api-view-2/', my_api_view, name='my-api-view-2'),
    path('user/', UserAPI.as_view(), name='user'),
    path('user-protected/', UserAPIProtected.as_view(), name='user-protected'),
    path('sample/', SimpleAPI.as_view(), name='sample'),
    path('books-generic/', BookGenericView.as_view(), name='books-generic'),
    path('books-generic/<int:pk>/', BookGenericRetrieve.as_view(), name='book-generic'),
    path('books-cached/', BookCachedAPI.as_view(), name='books-cached'),
]

# https://www.django-rest-framework.org/api-guide/routers/

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='books')
router.register(r'books-model', BookModelViewSet, basename='books-model')
router.register(r'books-paginated', BookPaginatedReadOnlyModelViewSet, basename='books-paginated')
# router.register(r'books-cached', BookCachedPaginated, basename='books-cached')
urlpatterns += router.urls  # or alternatively path('', include(router.urls))

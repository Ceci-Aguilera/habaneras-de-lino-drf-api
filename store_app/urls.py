from django.urls import re_path
from .views import *

app_name = 'store_app'

urlpatterns = [
    re_path('clothing-products/(?P<page>[^/]*)/$', ClothingProductListAPIView.as_view(),
            name='clothing-products-api-list'),
    re_path('clothing-collections/$', ClothingCollectionListAPIView.as_view(),
            name='clothing-collections-api-list'),
]

from django.urls import re_path
from .views import *

app_name = 'store_app'

urlpatterns = [
    re_path('clothing-products/(?P<page>[^/]*)/$', ClothingProductListAPIView.as_view(),
            name='clothing-products-api-list'),
    re_path('clothing-products/items/(?P<id>[0-9]+)/$', ClothingProductDetailAPIView.as_view(),
            name='clothing-products-api-detail'),
    re_path('clothing-collections/$', ClothingCollectionListAPIView.as_view(),
            name='clothing-collections-api-list'),
    re_path('clothing-collections/filter/names/$', ClothingCollectionsByNameYearLisAPIView.as_view(),
            name='clothing-collections-api-list'),
    re_path('clothing-collections/(?P<id>[0-9]+)/$', ClothingCollectionDetailAPIView.as_view(),
            name='clothing-collections-api-detail'),
    re_path('categories/$', CategoryListAPIView.as_view(), name='categories-api-list'),
    re_path('categories/(?P<id>[0-9]+)/$', CategoryDetailAPIView.as_view(), name='categories-api-detail'),
]

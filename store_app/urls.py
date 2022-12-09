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
    re_path('clothing-collections/filter/names/$', ClothingCollectionsByNameYearListAPIView.as_view(),
            name='clothing-collections-filter-name-api-list'),
    re_path('clothing-collections/(?P<id>[0-9]+)/$', ClothingCollectionDetailAPIView.as_view(),
            name='clothing-collections-api-detail'),
    re_path('categories/$', CategoryListAPIView.as_view(), name='categories-api-list'),
    re_path('categories/(?P<id>[0-9]+)/$', CategoryDetailAPIView.as_view(), name='categories-api-detail'),
    re_path('categories/filter/names/$', CategoriesByNameListAPIView.as_view(),
            name='categories-filter-name-api-list'),
    re_path('product-variations/$', ProductVariationCreateAPIView.as_view(), name='product-variation-api-create'),
    re_path('cart/(?P<token>[0-9A-Za-z_\-]+)/$', CartDetailAPIView.as_view(), name='cart-api-detail'),
    re_path('product-variations/(?P<id>[0-9]+)/$', ProductVariationRetrieveUpdateDeleteAPIView.as_view(),
            name='product-variations-api-detail-update-delete'),
    re_path('orders/$', OrderCreateAPIView.as_view(), name='orders-create')
]

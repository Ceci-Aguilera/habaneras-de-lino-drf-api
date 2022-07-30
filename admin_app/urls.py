from django.contrib import admin
from django.urls import re_path, include
from django.views.generic.base import TemplateView
from .views import *

app_name = 'admin_app'

urlpatterns = [
    re_path(r'^accounts/', include("django.contrib.auth.urls")),
    re_path(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    # Collections
    re_path(r'^collections/create/$', ClothingCollectionCreate.as_view(), name='collection-create'),
    re_path('collections/$', ClothingCollectionList.as_view(), name='collection-list'),
    re_path('collections/(?P<pk>[^/]*)/delete/$', ClothingCollectionDelete.as_view(), name='collection-delete'),
    re_path(r'^collections/(?P<pk>[^/]*)/update/$', ClothingCollectionUpdate.as_view(), name='collection-update'),
    # Categories
    re_path(r'^categories/create/$', CategoryCreate.as_view(), name='category-create'),
    re_path('categories/$', CategoryList.as_view(), name='category-list'),
    re_path('categories/(?P<pk>[^/]*)/delete/$', CategoryDelete.as_view(), name='category-delete'),
    re_path(r'^categories/(?P<pk>[^/]*)/update/$', CategoryUpdate.as_view(), name='category-update'),
    # Global Config
    re_path(r'^global-configs/create/$', GlobalConfigCreate.as_view(), name='global-config-create'),
    re_path('global-configs/$', GlobalConfigList.as_view(), name='global-config-list'),
    re_path(r'^global-configs/(?P<pk>[^/]*)/update/$', GlobalConfigUpdate.as_view(), name='global-config-update'),
    re_path(r'^global-configs/(?P<pk>[^/]*)/delete/$', GlobalConfigDelete.as_view(), name='global-config-delete'),
    # Custom Color
    re_path(r'^custom-colors/create/$', CustomColorCreate.as_view(), name='custom-color-create'),
    re_path('custom-colors/$', CustomColorList.as_view(), name='custom-color-list'),
    re_path(r'^custom-colors/(?P<pk>[^/]*)/update/$', CustomColorUpdate.as_view(), name='custom-color-update'),
    re_path(r'^custom-colors/(?P<pk>[^/]*)/delete/$', CustomColorDelete.as_view(), name='custom-color-delete'),
    # Clothing Product
    re_path(r'^clothing-products/create/$', ClothingProductCreate.as_view(), name='clothing-product-create'),
    re_path('clothing-products/$', ClothingProductList.as_view(), name='clothing-product-list'),
    re_path(r'^clothing-products/(?P<pk>[^/]*)/update/$', ClothingProductUpdate.as_view(),
            name='clothing-product-update'),
    re_path(r'^clothing-products/(?P<pk>[^/]*)/delete/$', ClothingProductDelete.as_view(),
            name='clothing-product-delete'),
    re_path(r'^collections/(?P<pk>[^/]*)/clothing-products/$', ClothingProductFilterCollection.as_view(),
            name='clothing-products-collection-filter'),
    re_path(r'^categories/(?P<pk>[^/]*)/clothing-products/$', ClothingProductFilterCategory.as_view(),
            name='clothing-products-category-filter'),
]

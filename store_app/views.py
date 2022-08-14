from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

import json
from datetime import datetime
from random import randint

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import *
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from .models import *
from .serializers import *

# =====================================================
#   PRODUCTS
# =====================================================


class ProductsPagination(PageNumberPagination):
    page_size = 16
    page_size_query_param = 'page_size'


class ClothingProductListAPIView(ListAPIView):
    authentication_classes = []
    serializer_class = ClothingProductSimpleSerializer
    model = ClothingProduct
    queryset = ClothingProduct.objects.all()
    pagination_class = ProductsPagination

    def get_serializer_context(self):
        context = super(ClothingProductListAPIView, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class ClothingProductDetailAPIView(RetrieveAPIView):
    authentication_classes = []
    serializer_class = ClothingProductSimpleSerializer
    model = ClothingProduct
    lookup_field = 'id'
    queryset = ClothingProduct.objects.all()
    pagination_class = None

    def get_serializer_context(self):
        context = super(ClothingProductDetailAPIView, self).get_serializer_context()
        context.update({"request": self.request})
        return context


# =====================================================
#   COLLECTIONS
# =====================================================


class ClothingCollectionListAPIView(ListAPIView):
    authentication_classes = []
    serializer_class = ClothingCollectionSerializer
    model = ClothingCollection
    queryset = ClothingCollection.objects.all()
    pagination_class = None

    def get_serializer_context(self):
        context = super(ClothingCollectionListAPIView, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class ClothingCollectionsByNameYearLisAPIView(ListAPIView):
    authentication_classes = []
    serializer_class = ClothingCollectionSerializer
    model = ClothingCollection
    pagination_class = None

    def get_queryset(self):
        queryset = ClothingCollection.objects.all()
        return queryset

    def get_serializer_context(self):
        context = super(ClothingCollectionsByNameYearLisAPIView, self).get_serializer_context()
        context.update({"request": self.request})
        return context
    
    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ClothingCollectionDetailAPIView(RetrieveAPIView):
    authentication_classes = []
    serializer_class = ClothingCollectionSerializer
    model = ClothingCollection
    lookup_field = 'id'
    queryset = ClothingCollection.objects.all()
    pagination_class = None

    def get_serializer_context(self):
        context = super(ClothingCollectionDetailAPIView, self).get_serializer_context()
        context.update({"request": self.request})
        return context


# =====================================================
#   CATEGORIES
# =====================================================


class CategoryListAPIView(ListAPIView):
    authentication_classes = []
    serializer_class = CategorySerializer
    model = Category
    queryset = Category.objects.all()
    pagination_class = None

    def get_serializer_context(self):
        context = super(CategoryListAPIView, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class CategoryDetailAPIView(RetrieveAPIView):
    authentication_classes = []
    serializer_class = CategorySerializer
    model = Category
    lookup_field = 'id'
    queryset = Category.objects.all()
    pagination_class = None

    def get_serializer_context(self):
        context = super(CategoryDetailAPIView, self).get_serializer_context()
        context.update({"request": self.request})
        return context
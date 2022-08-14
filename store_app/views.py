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


# =====================================================
#   CATEGORIES
# =====================================================


class ProductVariationCreateAPIView(CreateAPIView):
    authentication_classes = []
    serializer_class = ProductVariationSerializer
    model = ProductVariation

    def get_serializer_context(self):
        context = super(ProductVariationCreateAPIView, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        product_variation = serializer.save()
        product_amount = product_variation.quantity + product_variation.product.base_pricing
        token = self.request.data['cart_token']

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ipaddress = x_forwarded_for.split(',')[-1].strip()
        else:
            ipaddress = request.META.get('REMOTE_ADDR')

        try:
            cart = Cart.objects.get(ip_address=ipaddress, token=token)
            cart.total_amount = cart.total_amount + product_amount
        except:
            new_token = urlsafe_base64_encode(force_bytes(randint(1,999999)))
            cart = Cart(token=new_token, total_amount=product_amount)

        cart.save()
        product_variation.cart = cart
        product_variation.save()
        cart_serializer = CartSerializer(cart,  context={"request": request})
        return Response(cart_serializer.data, status=status.HTTP_201_CREATED)
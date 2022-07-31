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

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
import decimal

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import *
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from .models import *
from .serializers import *

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

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


class ClothingCollectionsByNameYearListAPIView(ListAPIView):
    authentication_classes = []
    serializer_class = ClothingCollectionSerializer
    model = ClothingCollection
    pagination_class = None

    def get_queryset(self):
        name = list(self.request.data['name'])
        year = self.request.data['year']
        queryset = ClothingCollection.objects.filter(title__in=name, year=year)
        return queryset

    def get_serializer_context(self):
        context = super(ClothingCollectionsByNameYearListAPIView, self).get_serializer_context()
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


class CategoriesByNameListAPIView(ListAPIView):
        authentication_classes = []
        serializer_class = CategorySerializer
        model = Category
        pagination_class = None

        def get_queryset(self):
            name = list(self.request.data['name'])
            queryset = Category.objects.filter(title__in=name)
            return queryset

        def get_serializer_context(self):
            context = super(CategoriesByNameListAPIView, self).get_serializer_context()
            context.update({"request": self.request})
            return context

        def post(self, request, *args, **kwargs):
            return self.list(request, *args, **kwargs)


# =====================================================
#   PRODUCT VARIATION
# =====================================================


class ProductVariationCreateAPIView(CreateAPIView):
    authentication_classes = []
    serializer_class = ProductVariationCreateSerializer
    model = ProductVariation

    def get_serializer_context(self):
        context = super(ProductVariationCreateAPIView, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        # serializer.is_valid(raise_exception=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        product_variation = serializer.save()

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ipaddress = x_forwarded_for.split(',')[-1].strip()
        else:
            ipaddress = request.META.get('REMOTE_ADDR')

        try:
            token = self.request.data['cart_token']
            cart = Cart.objects.get(ip_address=ipaddress, token=token, is_active=True)
        except:
            new_token = urlsafe_base64_encode(force_bytes(randint(1,999999)))
            cart = Cart(ip_address=ipaddress, token=new_token)

        cart.save()
        product_variation.cart = cart
        product_variation.save()
        cart_serializer = CartSerializer(cart,  context={"request": request})
        return Response(cart_serializer.data, status=status.HTTP_201_CREATED)


class ProductVariationRetrieveUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = []
    model = ProductVariation
    lookup_field = 'id'
    queryset = ProductVariation.objects.all()
    pagination_class = None

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            self.serializer_class = ProductVariationCreateSerializer
        else:
            self.serializer_class = ProductVariationSerializer
        return self.serializer_class

    def get_serializer_context(self):
        context = super(ProductVariationRetrieveUpdateDeleteAPIView, self).get_serializer_context()
        context.update({"request": self.request})
        return context



# =====================================================
#   CART
# =====================================================


class CartDetailAPIView(RetrieveAPIView):
    authentication_classes = []
    serializer_class = CartSerializer
    model = Cart
    lookup_field = 'token'
    queryset = Cart.objects.all()
    pagination_class = None

    def get_serializer_context(self):
        context = super(CartDetailAPIView, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_object(self):
        token = self.kwargs.get(self.lookup_field)
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ipaddress = x_forwarded_for.split(',')[-1].strip()
        else:
            ipaddress = self.request.META.get('REMOTE_ADDR')

        try:
            cart = Cart.objects.get(ip_address=ipaddress, token=token, is_active=True)
        except:
            cart = None
        return cart


# =====================================================
#   ORDER
# =====================================================


class OrderCreateAPIView(CreateAPIView):
    authentication_classes = []
    serializer_class = OrderSerializer
    model = Order

    def get_serializer_context(self):
        context = super(OrderCreateAPIView, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def post(self, request):
        serializer = self.serializer_class(data=self.request.data)
        if not serializer.is_valid():
            return Response({'Result': 'Personal information is not valid'}, status=status.HTTP_400_BAD_REQUEST)
        shipping_address_serializer = AddressSerializer(data=request.data['shipping_address'])
        if not shipping_address_serializer.is_valid():
            return Response({'Result': 'Shipping information is not valid'}, status=status.HTTP_400_BAD_REQUEST)
        shipping_address = shipping_address_serializer.save()
        order = serializer.save(shipping_address=shipping_address, other_costs=Decimal(0.0000), shipping_cost=Decimal(0.0000))

        #Try making payment
        try:
            card_num = request.data['card_num']
            exp_month = request.data['exp_month']
            exp_year = request.data['exp_year']
            cvc = request.data['cvc']

            token = stripe.Token.create(
                card={
                    "number": card_num,
                    "exp_month": int(exp_month),
                    "exp_year": int(exp_year),
                    "cvc": cvc
                },
            )

            amount = float(order.cart.total_amount + order.cart.total_amount * decimal.Decimal(0.07))
            amount = int(amount * 100)
            shipping_dictionary = {
                'address': {
                    'city': order.shipping_address.city,
                    'country': 'United States',
                    'line1': order.shipping_address.street,
                    'line2': order.shipping_address.apt_suite,
                    'postal_code': order.shipping_address.zip_code,
                    'state': order.shipping_address.usa_state,
                },
                'name': order.first_name + " " + order.last_name,
                'phone': order.phone if order.phone else '---'
            }

            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=token,
                shipping=shipping_dictionary,
                receipt_email=order.email
            )

            stripe_charge_id = charge['id']
            amount = amount / 100
            payment = Payment(email=order.email, ip_address=order.cart.ip_address, stripe_charge_id=stripe_charge_id,
                              amount=amount)

            payment.save()
            order.ordered = True
            order.payment = payment
            order.save()
            order.cart.last = False
            order.cart.save()

            return Response({"Result": "Success"}, status=status.HTTP_200_OK)

        except stripe.error.CardError as e:
            order.delete()
            return Response({"Result": "Error with card during payment"}, status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.RateLimitError as e:
            order.delete()
            return Response({"Result": "Rate Limit error during payment"}, status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.InvalidRequestError as e:
            order.delete()
            return Response({"Result": "Invalid request error during payment"}, status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.AuthenticationError as e:
            order.delete()
            return Response({"Result": "Authentication error during payment"}, status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.APIConnectionError as e:
            order.delete()
            return Response({"Result": "API connection error during payment"}, status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.StripeError as e:
            order.delete()
            return Response({"Result": "Something went wrong during payment"}, status=status.HTTP_400_BAD_REQUEST)

        except:
            order.delete()
            return Response({"Result": "Error during payment"}, status=status.HTTP_400_BAD_REQUEST)

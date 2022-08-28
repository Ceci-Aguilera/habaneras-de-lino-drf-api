from rest_framework import serializers
from .models import *


class ProductImageSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField('get_image')

    def get_image(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.image.url)

    class Meta:
        model = ClothingProductImage
        fields = '__all__'


class CustomColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomColor
        fields = '__all__'


class ClothingProductSimpleSerializer(serializers.ModelSerializer):

    primary_image = serializers.SerializerMethodField('get_primary_image')
    secondary_image = serializers.SerializerMethodField('get_secondary_image')
    extra_images = serializers.SerializerMethodField('get_extra_images')
    available_colors = CustomColorSerializer(many=True)

    def get_primary_image(self, obj):
        serializer_context = {'request': self.context.get('request')}
        image = ClothingProductImage.objects.get(type_of_image="PRIMARY", product=obj)
        return ProductImageSerializer(image, context=serializer_context).data

    def get_secondary_image(self, obj):
        serializer_context = {'request': self.context.get('request')}
        image = ClothingProductImage.objects.get(type_of_image="SECONDARY", product=obj)
        return ProductImageSerializer(image, context=serializer_context).data

    def get_extra_images(self, obj):
        serializer_context = {'request': self.context.get('request')}
        images = ClothingProductImage.objects.filter(type_of_image="EXTRA", product=obj)
        return ProductImageSerializer(images, many=True, context=serializer_context).data

    class Meta:
        model = ClothingProduct
        fields = ['id', 'name', 'available_colors', 'tag', 'code', 'collections', 'categories', 'base_pricing',
                  'primary_image', 'secondary_image', 'extra_images']


class ClothingCollectionSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField('get_image')
    products = serializers.SerializerMethodField('get_products')

    def get_products(self, obj):
        serializer_context = {'request': self.context.get('request')}
        clothing_products = obj.clothing_products.all()
        return ClothingProductSimpleSerializer(clothing_products, many=True, context=serializer_context).data

    def get_image(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.image.url)

    class Meta:
        model = ClothingCollection
        fields = ['title', 'description', 'year', 'image', 'products', 'id', ]


class CategorySerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField('get_image')
    products = serializers.SerializerMethodField('get_products')

    def get_products(self, obj):
        serializer_context = {'request': self.context.get('request')}
        clothing_products = obj.clothing_products.all()
        return ClothingProductSimpleSerializer(clothing_products, many=True, context=serializer_context).data

    def get_image(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.image.url)

    class Meta:
        model = ClothingCollection
        fields = ['title', 'description', 'image', 'products', 'id', ]


class ProductVariationSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField('get_product')
    principal_color =  CustomColorSerializer()

    def get_product(self, obj):
        serializer_context = {'request': self.context.get('request')}
        clothing_product = obj.product
        return ClothingProductSimpleSerializer(clothing_product, context=serializer_context).data

    class Meta:
        model = ProductVariation
        fields = '__all__'


class ProductVariationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductVariation
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):

    product_variations = serializers.SerializerMethodField('get_product_variations')

    def get_product_variations(self, obj):
        serializer_context = {'request': self.context.get('request')}
        product_variations = ProductVariation.objects.filter(cart=obj)
        return ProductVariationSerializer(product_variations, many=True, context=serializer_context).data

    class Meta:
        model = Cart
        fields = ['id', 'total_amount', 'created_date', 'is_active', 'token', 'product_variations']

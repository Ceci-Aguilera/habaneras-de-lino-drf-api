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


class ClothingProductSimpleSerializer(serializers.ModelSerializer):

    primary_image = serializers.SerializerMethodField('get_primary_image')
    secondary_image = serializers.SerializerMethodField('get_secondary_image')
    extra_images = serializers.SerializerMethodField('get_extra_images')

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
        fields = ['name', 'collections', 'categories', 'base_pricing', 'primary_image', 'secondary_image',
                  'extra_images']

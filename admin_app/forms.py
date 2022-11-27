from django.forms import ModelForm
from django.forms.widgets import TextInput

from store_app.models import *


class CollectionForm(ModelForm):
    class Meta:
        model = ClothingCollection
        fields = '__all__'
        labels = {
            'title': 'Nombre de la coleccion',
            'year': 'Año',
            'description': 'Descripcion de la coleccion',
            'image': 'Imagen principal de la coleccion'
        }


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        labels = {
            'title': 'Nombre de la categoria',
            'description': 'Descripcion de la categoria',
            'image': 'Imagen principal de la categoria'
        }


class GlobalConfigForm(ModelForm):
    class Meta:
        model = GlobalModel
        fields = '__all__'
        labels = {
            'active': 'Activo',
            'mx_value': 'Valor del peso Mexicano',
            'us_sales_taxes': 'Taxes para ventas'
        }
        help_texts = {
            'active': 'Si esta activa, esta configuracion se utilizara como informacion de pagos',
            'mx_value': 'El valor del peso Mexicano con respoecto al dolar. Si 25 pesos Mexicanos equivalen a un dolar,'
                        ' escriba 25.00 en campo en blanco',
            'us_sales_taxes': 'Taxes a aplicar durante una compra. En la Florida es 0.07',
        }


class CustomColorForm(ModelForm):
    class Meta:
        model = CustomColor
        fields = '__all__'
        widgets = {
            'code': TextInput(attrs={'type': 'color'}),
        }
        labels = {
            'nickname': 'Nombre del color',
            'code': 'Codigo',
        }
        help_texts = {
            'code': 'Codigo en hexadecimal (#aaa, #aaaaaa, #aaaaaaaa)',
        }


class ClothingProductForm(ModelForm):
    class Meta:
        model = ClothingProduct
        fields = '__all__'
        labels = {
            'name': 'Nombre del prooducto',
            'code': 'Codigo',
            'collections': 'Colecciones',
            'categories': 'Categorias',
            'available_colors': 'Colores disponibles',
            'base_pricing': 'Precio base',
            'amount_sold': 'Cantidad Vendida'
        }


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ('cart', 'email', 'phone', 'first_name', 'last_name', 'status',
                  'shipping_address', 'shipping_tracking_id', 'comments')
        labels = {
            'cart': 'Carrito',
            'email': 'Email del cliente',
            'phone': 'Celular del cliente',
            'first_name': 'Nombre del cliente',
            'last_name': 'Apellido del cliente',
            'shipping_address': 'Direccion del cliente',
            'shipping_tracking_id': 'ID del shipping (UPS/Fedex)',
            'status': 'Estado de la orden',
            'comments': 'Commentarios a tener en cuenta para la orden'
        }


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = ('email', 'stripe_charge_id', 'amount', 'refund')
        labels = {
            'email': 'Email del cliente',
            'stripe_charge_id': 'ID de pago en Stripe',
            'amount': 'Cantidad (incluye taxes + shipping)',
            'refund': 'Refund',
        }

from django.db.models import DecimalField
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

"""
    The Currency Field is a more accurate Decimal Field for managing a positive amount of payment and easily calculate
    taxes and the conversion to the MX
"""


def validate_positive(value):
    if value < 0:
        raise ValidationError(
            _("%(value)s is not positive."),
            params={"value": value}
        )


class CurrencyDecimalField(DecimalField):
    description = _("A custom decimal field")

    def __init__(self, *args, **kwargs):
        kwargs['default'] = Decimal("0.00")
        kwargs['max_digits'] = 19
        kwargs['decimal_places'] = 4
        super().__init__(*args, **kwargs)

    @cached_property
    def validators(self):
        return super().validators + [validate_positive]


IMAGE_CHOICES = (
    ('PRIMARY', 'PRIMARY'),
    ('SECONDARY', 'SECONDARY'),
    ('EXTRA', 'EXTRA')
)

TAG_OPTIONS = (
    ('SHIRT', 'SHIRT'),
    ('PANTS', 'PANTS'),
    ('DRESS', 'DRESS')
)

USA_STATE_CHOICES = (
    (("Alabama", "Alabama"), ("Alaska", "Alaska"), ("Arizona", "Arizona"), ("Arkansas", "Arkansas"),
     ("California", "California"), ("Colorado", "Colorado"), ("Connecticut", "Connecticut"), ("Delaware", "Delaware"),
     ("Florida", "Florida"), ("Georgia", "Georgia"), ("Hawaii", "Hawaii"), ("Idaho", "Idaho"), ("Illinois", "Illinois"),
     ("Indiana", "Indiana"), ("Iowa", "Iowa"), ("Kansas", "Kansas"), ("Kentucky", "Kentucky"),
     ("Louisiana", "Louisiana"), ("Maine", "Maine"), ("Maryland", "Maryland"), ("Massachusetts", "Massachusetts"),
     ("Michigan", "Michigan"), ("Minnesota", "Minnesota"), ("Mississippi", "Mississippi"), ("Missouri", "Missouri"),
     ("Montana", "Montana"), ("Nebraska", "Nebraska"), ("Nevada", "Nevada"), ("New Hampshire", "New Hampshire"),
     ("New Jersey", "New Jersey"), ("New Mexico", "New Mexico"), ("New York", "New York"),
     ("North Carolina", "North Carolina"), ("North Dakota", "North Dakota"), ("Ohio", "Ohio"), ("Oklahoma", "Oklahoma"),
     ("Oregon", "Oregon"), ("Pennsylvania", "Pennsylvania"), ("Rhode Island", "Rhode Island"),
     ("South Carolina", "South Carolina"), ("South Dakota", "South Dakota"), ("Tennessee", "Tennessee"),
     ("Texas", "Texas"), ("Utah", "Utah"), ("Vermont", "Vermont"), ("Virginia", "Virginia"),
     ("Washington", "Washington"), ("West Virginia", "West Virginia"), ("Wisconsin", "Wisconsin"),
     ("Wyoming", "Wyoming"))
)

REFUND_STATUS_CHOICES = (
    ('NO REFUND ASKED', 'NO REFUND ASKED'),
    ('REFUND REQUESTED', 'REFUND REQUESTED'),
    ('REFUND MADE', 'REFUND MADE'),
    ('REFUND FAILED', 'REFUND FAILED')
)

ORDER_STATUS_CHOICES = (
    ('ORDEN_CREADA', 'ORDEN_CREADA'),
    ('PEDIDO_A_MEXICO', 'PEDIDO_A_MEXICO'),
    ('EN_CAMINO', 'EN_CAMINO'),
    ('ENTREGADO', 'ENTREGADO'),
    ('CANCELADO', 'CANCELADO'),
    ('REFUND', 'REFUND')
)
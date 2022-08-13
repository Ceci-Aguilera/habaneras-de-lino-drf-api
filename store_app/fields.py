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
from django.db.models import Model, DecimalField
from django.core.validators import MinValueValidator, MaxValueValidator


class DiscountMixin(Model):
    discount_percent = DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Input format like 0.25 (25%)",
    )

    class Meta:
        abstract = True

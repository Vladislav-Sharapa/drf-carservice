from django_filters.filterset import FilterSet

from supplier.models import CarModel


class CarFilter(FilterSet):
    class Meta:
        model = CarModel
        exclude = ["id", "updated_at", "created_at"]

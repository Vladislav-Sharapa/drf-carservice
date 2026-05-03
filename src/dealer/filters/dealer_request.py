from django_filters.rest_framework import FilterSet

from dealer.models import DealerShipRequest


class DealerRequestFilter(FilterSet):
    class Meta:
        model = DealerShipRequest
        fields = ["status"]

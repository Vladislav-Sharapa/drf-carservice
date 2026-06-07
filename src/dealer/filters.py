from datetime import date

from django_filters.filterset import FilterSet
from django_filters import DateFilter, MultipleChoiceFilter
from django.db.models.query import QuerySet

from core.enums import TransactionStatusEnum


class OrderFilter(FilterSet):
    start_date = DateFilter(method="filter_start_date")
    end_date = DateFilter(method="filter_end_date")
    status = MultipleChoiceFilter(
        field_name="status",
        choices=TransactionStatusEnum.choices,
    )

    def filter_start_date(self, queryset: QuerySet, name: str, value: date):
        if value:
            return queryset.filter(created_at__gte=value)
        return queryset

    def filter_end_date(self, queryset: QuerySet, name: str, value: date):
        if value:
            return queryset.filter(created_at__lte=value)
        return queryset

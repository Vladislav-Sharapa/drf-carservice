from typing import Any, Literal
from uuid import UUID

from core.services import BaseService
from dealer.models import DealerShip
from rest_framework.exceptions import NotFound
from django.db.models import QuerySet


class DealerShipService(BaseService):
    model = DealerShip

    def get_requests(self, dealership_id: UUID, filters: dict) -> QuerySet:
        return self._get_dealer_related_queryset(
            dealership_id, "requests", "car", filters
        )

    def get_inventory(self, dealership_id: UUID) -> QuerySet:
        return self._get_dealer_related_queryset(dealership_id, "inventory", "car")

    def get_promotions(self, dealership_id: UUID) -> QuerySet:
        return self._get_dealer_related_queryset(dealership_id, "promotions")

    def get_loyalty_discount(self, dealership_id: UUID) -> QuerySet:
        return self._get_dealer_related_queryset(dealership_id, "loyalty_discount")

    def _get_dealer_related_queryset(
        self,
        dealership_id: UUID,
        attr_name: Literal["requests", "inventory", "promotions", "loyalty_discount"],
        select_related_field: str = None,
        filters: dict[str, Any] = None,
    ) -> QuerySet:
        """Return a queryset of related objects for a dealership

        Args:
            dealership_id: ID of dealer
            attr_name: Name of the related attribute on the dealership model
            select_related_field: Name of select_related_field

        Raises:
            NotFound: If the dealership is not found by the given `dealership_id`
            or if the related collection is empty.

        Returns:
            Sequence: A sequence of related objects
        """
        dealership = self.get_by_id(dealership_id)
        queryset: QuerySet = getattr(dealership, attr_name).select_related(
            select_related_field
        )
        queryset = self._apply_filters(queryset, filters)

        if not queryset:
            raise NotFound
        return queryset

    def _apply_filters(self, queryset: QuerySet, filters: dict):
        print(filters)
        if filters:
            for field, value in filters.items():
                queryset = queryset.filter(**{field: value})
        return queryset

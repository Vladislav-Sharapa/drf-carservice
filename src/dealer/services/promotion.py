from datetime import datetime
from decimal import Decimal
from typing import Sequence
from uuid import UUID

from django.db import IntegrityError

from core.services import BaseService
from dealer.exceptions import PromotionDateException
from dealer.models import DealerShip, DealerShipPromotion
from rest_framework.exceptions import APIException, NotFound


class DealerPromotionService(BaseService):
    model = DealerShipPromotion

    def get_by_dealer_id(self, dealer_id: UUID) -> Sequence:
        instances = DealerShipPromotion.objects.filter(dealership_id=dealer_id)
        if not instances.exists():
            raise NotFound(
                detail=f"There is no dealership promotions with dealearhip id:{dealer_id}"
            )
        return instances

    def create(
        self,
        name: str,
        dealership: DealerShip,
        start_date: datetime,
        end_date: datetime,
        discount_percent: Decimal,
    ):
        if end_date == start_date:
            raise PromotionDateException
        try:
            instance = DealerShipPromotion.objects.create(
                name=name,
                dealership_id=dealership.id,
                start_date=start_date,
                end_date=end_date,
                discount_percent=discount_percent,
            )
        except IntegrityError as e:
            raise APIException(detail=f"Internal server error. Detail {e}")
        return instance

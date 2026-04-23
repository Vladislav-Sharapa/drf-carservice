from rest_framework.viewsets import ViewSet

from core.mixins.views import UpdateModelMixin
from dealer.serializers.inventory import DealerInventoryUpdateSerializer
from dealer.services.inventory import DealerShipInventoryService


class DealerInventoryUpdateViewSet(ViewSet, UpdateModelMixin):
    service = DealerShipInventoryService()
    serializer_class = DealerInventoryUpdateSerializer

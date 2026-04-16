from core.services import BaseService
from dealer.models import DealerShip


class DealerShipService(BaseService):
    model = DealerShip

from core.services import BaseService
from supplier.models import CarModel


class CarService(BaseService):
    model = CarModel

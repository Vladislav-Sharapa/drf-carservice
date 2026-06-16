from core.services import BaseService
from supplier.models import Supplier


class SupplierService(BaseService):
    model = Supplier

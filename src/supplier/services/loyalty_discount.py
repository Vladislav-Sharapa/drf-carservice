from core.services import BaseService
from supplier.models import SupplierLoyaltyDiscount


class SupplierLoyaltyDiscountService(BaseService):
    model = SupplierLoyaltyDiscount

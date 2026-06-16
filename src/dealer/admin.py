from django.contrib import admin

from dealer.models import (
    DealerShip,
    DealerShipRequest,
    DealerShipInventory,
    DealerShipPromotion,
)

admin.site.register(DealerShip)
admin.site.register(DealerShipRequest)
admin.site.register(DealerShipInventory)
admin.site.register(DealerShipPromotion)

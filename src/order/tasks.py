from celery import shared_task

from order.services.order import OrderService
from celery import group
from order.flows.order import OrderProcessingFlow


@shared_task
def find_orders(status: str):
    service = OrderService()
    orders = service.get_by_status(status)
    if not orders:
        return None
    tasks_group = [search_best_auto_offers.s(order.id) for order in orders]
    jobs = group(tasks_group)
    jobs.apply_async()
    return len(tasks_group)


@shared_task
def search_best_auto_offers(id: int):
    order_service = OrderService()
    order = order_service.get_by_id(id)
    service = OrderProcessingFlow()
    service.execute(order=order)

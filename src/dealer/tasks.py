from celery import shared_task

from dealer.flows.dealer_request import DealerRequestProcessFlow
from dealer.services.dealer_reqeust import DealerShipRequestService
from celery import group


@shared_task
def find_dealer_requests(status: str):
    service = DealerShipRequestService()
    requests = service.get_by_status(status)
    if not requests:
        return None
    tasks_group = [search_best_auto_request.s(request.id) for request in requests]
    jobs = group(tasks_group)
    jobs.apply_async()
    return len(tasks_group)


@shared_task
def search_best_auto_request(id: int):
    request_service = DealerShipRequestService()
    request = request_service.get_by_id(id)
    service = DealerRequestProcessFlow()
    service.execute(request=request)

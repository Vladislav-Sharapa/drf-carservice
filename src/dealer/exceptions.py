from rest_framework.exceptions import APIException
from rest_framework import status


class NotPendingReqestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Processing not pending request"

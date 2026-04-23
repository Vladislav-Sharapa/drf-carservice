from rest_framework.exceptions import APIException
from rest_framework import status


class NegativeInventoryCountException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Count of objects must not be less than zero"


class DuplicateInventoryException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Requested inventory record already exists in the database"


class NegativeBalanceException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Balance must be positive"


class PromotionDateException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "End date of promotion must be greater than start date"

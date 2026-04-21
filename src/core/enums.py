from django.db.models import TextChoices


class TransactionStatusEnum(TextChoices):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    ERROR = "ERROR"
    FAILED = "FAILED"

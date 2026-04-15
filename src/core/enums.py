from django.db.models import TextChoices


class TransactionStatusEnum(TextChoices):
    PENDING = "pending"
    PROCESSING = "processing"
    ERROR = "error"
    FAILED = "failed"

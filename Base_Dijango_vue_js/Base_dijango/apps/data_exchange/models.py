from django.conf import settings
from django.db import models


class ImportJob(models.Model):
    class Status(models.TextChoices):
        VALIDATING = "validating", "Đang kiểm tra"
        READY = "ready", "Sẵn sàng xác nhận"
        INVALID = "invalid", "Có lỗi"
        STALE = "stale", "Dữ liệu đã thay đổi"
        CONFIRMED = "confirmed", "Đã ghi dữ liệu"

    class Mode(models.TextChoices):
        CREATE = "create", "Tạo mới"
        UPDATE = "update", "Cập nhật"
        UPSERT = "upsert", "Tạo hoặc cập nhật"

    module = models.CharField(max_length=40)
    mode = models.CharField(max_length=20, choices=Mode.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.VALIDATING)
    original_name = models.CharField(max_length=255)
    file_hash = models.CharField(max_length=64)
    file_content = models.BinaryField()
    template_version = models.CharField(max_length=20, default="1")
    total_rows = models.PositiveIntegerField(default=0)
    new_rows = models.PositiveIntegerField(default=0)
    update_rows = models.PositiveIntegerField(default=0)
    error_rows = models.PositiveIntegerField(default=0)
    preview = models.JSONField(default=list)
    dependency_fingerprint = models.CharField(max_length=64, blank=True)
    idempotency_key = models.CharField(max_length=100, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    validated_at = models.DateTimeField(null=True, blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["created_by", "status", "created_at"])]
        constraints = [
            models.UniqueConstraint(
                fields=["created_by", "idempotency_key"],
                condition=~models.Q(idempotency_key=""),
                name="exchange_unique_import_idempotency",
            )
        ]

    def __str__(self) -> str:
        return f"{self.module} · {self.original_name} · {self.status}"


class RowIssue(models.Model):
    job = models.ForeignKey(ImportJob, on_delete=models.CASCADE, related_name="issues")
    row_number = models.PositiveIntegerField()
    column = models.CharField(max_length=80, blank=True)
    field_code = models.CharField(max_length=80, blank=True)
    error_code = models.CharField(max_length=50)
    message = models.CharField(max_length=255)
    raw_value = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["row_number", "column"]

    def __str__(self) -> str:
        return f"Dòng {self.row_number} · {self.error_code}"

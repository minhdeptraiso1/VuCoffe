from rest_framework import serializers

from apps.data_exchange.models import ImportJob, RowIssue
from apps.data_exchange.services import SUPPORTED_MODULES


class RowIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = RowIssue
        fields = ["row_number", "column", "field_code", "error_code", "message", "raw_value"]


class ImportJobSerializer(serializers.ModelSerializer):
    issues = RowIssueSerializer(many=True, read_only=True)
    created_by_name = serializers.CharField(source="created_by.full_name", read_only=True)

    class Meta:
        model = ImportJob
        fields = [
            "id",
            "module",
            "mode",
            "status",
            "original_name",
            "total_rows",
            "new_rows",
            "update_rows",
            "error_rows",
            "preview",
            "issues",
            "created_by_name",
            "created_at",
            "validated_at",
            "confirmed_at",
        ]


class ImportUploadSerializer(serializers.Serializer):
    module = serializers.ChoiceField(choices=sorted(SUPPORTED_MODULES))
    mode = serializers.ChoiceField(choices=ImportJob.Mode.choices)
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.lower().endswith(".xlsx"):
            raise serializers.ValidationError("Chỉ chấp nhận file .xlsx.")
        return value


class ImportConfirmSerializer(serializers.Serializer):
    idempotency_key = serializers.CharField(max_length=100)

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdminRole
from apps.data_exchange.models import ImportJob
from apps.data_exchange.services import (
    build_error_workbook,
    build_template,
    confirm_import,
    create_import_job,
    export_module,
)

from .serializers import ImportConfirmSerializer, ImportJobSerializer, ImportUploadSerializer


def _xlsx_response(content: bytes, filename: str) -> HttpResponse:
    response = HttpResponse(
        content,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


class ImportTemplateView(APIView):
    permission_classes = [IsAdminRole]

    @extend_schema(
        tags=["Import/export"], responses={200: OpenApiResponse(description="XLSX template")}
    )
    def get(self, request, module: str):
        return _xlsx_response(build_template(module), f"{module}-template-v1.xlsx")


class ImportListCreateView(GenericAPIView):
    permission_classes = [IsAdminRole]
    serializer_class = ImportJobSerializer

    @extend_schema(tags=["Import/export"], responses={200: ImportJobSerializer(many=True)})
    def get(self, request):
        jobs = ImportJob.objects.filter(created_by=request.user).prefetch_related("issues")
        page = self.paginate_queryset(jobs)
        serializer = ImportJobSerializer(page if page is not None else jobs, many=True)
        return (
            self.get_paginated_response(serializer.data)
            if page is not None
            else Response(serializer.data)
        )

    @extend_schema(
        tags=["Import/export"], request=ImportUploadSerializer, responses={201: ImportJobSerializer}
    )
    def post(self, request):
        serializer = ImportUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        job = create_import_job(
            actor=request.user,
            module=serializer.validated_data["module"],
            mode=serializer.validated_data["mode"],
            uploaded_file=serializer.validated_data["file"],
        )
        return Response(ImportJobSerializer(job).data, status=status.HTTP_201_CREATED)


class ImportDetailView(APIView):
    permission_classes = [IsAdminRole]

    @extend_schema(tags=["Import/export"], responses={200: ImportJobSerializer})
    def get(self, request, job_id: int):
        job = get_object_or_404(
            ImportJob.objects.prefetch_related("issues"), id=job_id, created_by=request.user
        )
        return Response(ImportJobSerializer(job).data)


class ImportErrorWorkbookView(APIView):
    permission_classes = [IsAdminRole]

    @extend_schema(
        tags=["Import/export"],
        responses={200: OpenApiResponse(description="XLSX annotated errors")},
    )
    def get(self, request, job_id: int):
        job = get_object_or_404(
            ImportJob.objects.prefetch_related("issues"), id=job_id, created_by=request.user
        )
        return _xlsx_response(build_error_workbook(job), f"import-{job.id}-errors.xlsx")


class ImportConfirmView(APIView):
    permission_classes = [IsAdminRole]

    @extend_schema(
        tags=["Import/export"],
        request=ImportConfirmSerializer,
        responses={200: ImportJobSerializer},
    )
    def post(self, request, job_id: int):
        serializer = ImportConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        job = get_object_or_404(ImportJob, id=job_id, created_by=request.user)
        job = confirm_import(
            job=job,
            actor=request.user,
            idempotency_key=serializer.validated_data["idempotency_key"],
        )
        return Response(ImportJobSerializer(job).data)


class ExportView(APIView):
    permission_classes = [IsAdminRole]

    @extend_schema(
        tags=["Import/export"], responses={200: OpenApiResponse(description="XLSX export")}
    )
    def get(self, request, module: str):
        return _xlsx_response(export_module(module), f"{module}-export.xlsx")

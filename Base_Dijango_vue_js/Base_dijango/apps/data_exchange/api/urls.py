from django.urls import path

from .views import (
    ExportView,
    ImportConfirmView,
    ImportDetailView,
    ImportErrorWorkbookView,
    ImportListCreateView,
    ImportTemplateView,
)

urlpatterns = [
    path("imports/", ImportListCreateView.as_view(), name="import-list"),
    path("imports/templates/<str:module>/", ImportTemplateView.as_view(), name="import-template"),
    path("imports/<int:job_id>/", ImportDetailView.as_view(), name="import-detail"),
    path(
        "imports/<int:job_id>/error-file/",
        ImportErrorWorkbookView.as_view(),
        name="import-error-file",
    ),
    path("imports/<int:job_id>/confirm/", ImportConfirmView.as_view(), name="import-confirm"),
    path("exports/<str:module>/", ExportView.as_view(), name="export-module"),
]

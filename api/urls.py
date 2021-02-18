from .views import SeoReportView
from django.urls import path

urlpatterns = [
    path('seo_report', SeoReportView, name="seo_report"),
]

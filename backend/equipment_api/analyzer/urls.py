from django.urls import path
from .views import upload_csv,get_summary,get_history

urlpatterns = [
    path('upload/', upload_csv),
    path('summary/<int:dataset_id>/', get_summary),
    path('history/', get_history),
]

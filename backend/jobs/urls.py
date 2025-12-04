from django.urls import path
from .views import JobListCreateView, JobDetailView, RecruiterJobListView

urlpatterns = [
    path('jobs/', JobListCreateView.as_view(), name='job_list_create'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job_detail'),
    path('jobs/my-jobs/', RecruiterJobListView.as_view(), name='recruiter_jobs'),
]

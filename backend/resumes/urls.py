from django.urls import path
from .views import ResumeListCreateView, ResumeDetailView, ResumeAnalysisView

urlpatterns = [
    path('resumes/', ResumeListCreateView.as_view(), name='resume_list_create'),
    path('resumes/<int:pk>/', ResumeDetailView.as_view(), name='resume_detail'),
    path('resumes/<int:pk>/analysis/', ResumeAnalysisView.as_view(), name='resume_analysis'),
]

from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from .models import Job, JobSkill
from .serializers import JobSerializer, JobListSerializer, JobSkillSerializer
from users.models import User

class IsRecruiterOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow recruiters to edit their own jobs.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == User.UserRole.RECRUITER

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.recruiter == request.user

class JobListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsRecruiterOrReadOnly)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'location', 'recruiter__recruiter_profile__company_name']
    ordering_fields = ['created_at', 'salary_min', 'views_count']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return JobListSerializer
        return JobSerializer

    def get_queryset(self):
        queryset = Job.objects.filter(status=Job.JobStatus.ACTIVE)
        
        # Custom filtering
        job_type = self.request.query_params.get('job_type')
        if job_type:
            queryset = queryset.filter(job_type=job_type)
            
        experience_level = self.request.query_params.get('experience_level')
        if experience_level:
            queryset = queryset.filter(experience_level=experience_level)
            
        is_remote = self.request.query_params.get('is_remote')
        if is_remote:
            queryset = queryset.filter(is_remote=is_remote.lower() == 'true')
            
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        job = serializer.save(
            recruiter=self.request.user,
            posted_date=timezone.now(),
            status=Job.JobStatus.ACTIVE
        )
        
        # Handle skills if provided
        skills_data = request.data.get('skills', [])
        for skill_name in skills_data:
            JobSkill.objects.create(job=job, name=skill_name)
            
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"success": True, "data": serializer.data}, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"success": True, "data": serializer.data})

class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsRecruiterOrReadOnly,)
    serializer_class = JobSerializer
    queryset = Job.objects.all()
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Increment view count
        instance.increment_views()
        
        serializer = self.get_serializer(instance)
        return Response({"success": True, "data": serializer.data})
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"success": True, "data": serializer.data})
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = Job.JobStatus.CLOSED
        instance.save()
        return Response({"success": True, "message": "Job closed successfully"}, status=status.HTTP_200_OK)

class RecruiterJobListView(generics.ListAPIView):
    """List jobs posted by the current recruiter"""
    permission_classes = (permissions.IsAuthenticated, IsRecruiterOrReadOnly)
    serializer_class = JobListSerializer
    
    def get_queryset(self):
        return Job.objects.filter(recruiter=self.request.user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"success": True, "data": serializer.data})

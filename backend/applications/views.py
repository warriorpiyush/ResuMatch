from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Application, ApplicationStatusHistory
from .serializers import ApplicationSerializer, ApplicationListSerializer
from jobs.models import Job
from resumes.models import Resume
from matches.models import Match

class ApplicationListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ApplicationListSerializer
        return ApplicationSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'CANDIDATE':
            return Application.objects.filter(candidate=user).order_by('-applied_at')
        elif user.role == 'RECRUITER':
            return Application.objects.filter(job__recruiter=user).order_by('-applied_at')
        return Application.objects.none()

    def create(self, request, *args, **kwargs):
        if request.user.role != 'CANDIDATE':
            return Response(
                {"success": False, "message": "Only candidates can apply"}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        data = request.data.copy()
        job_id = data.get('job')
        resume_id = data.get('resume')
        
        # Validate job
        job = get_object_or_404(Job, id=job_id, status='ACTIVE')
        
        # Validate resume
        if not resume_id:
            # Use active resume if not provided
            resume = Resume.objects.filter(user=request.user, is_active=True).first()
            if not resume:
                return Response(
                    {"success": False, "message": "No active resume found"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            data['resume'] = resume.id
        else:
            resume = get_object_or_404(Resume, id=resume_id, user=request.user)
            
        # Check if already applied
        if Application.objects.filter(candidate=request.user, job=job).exists():
            return Response(
                {"success": False, "message": "Already applied to this job"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Get match score
        match_score = 0
        match = Match.objects.filter(resume=resume, job=job).first()
        if match:
            match_score = match.overall_score
            
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        application = serializer.save(
            candidate=request.user,
            match_score=match_score
        )
        
        # Increment job application count
        job.increment_applications()
        
        # Record history
        ApplicationStatusHistory.objects.create(
            application=application,
            old_status='',
            new_status=Application.ApplicationStatus.PENDING,
            changed_by=request.user,
            notes='Application submitted'
        )
        
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

class ApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ApplicationSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'CANDIDATE':
            return Application.objects.filter(candidate=user)
        elif user.role == 'RECRUITER':
            return Application.objects.filter(job__recruiter=user)
        return Application.objects.none()
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"success": True, "data": serializer.data})
    
    def update(self, request, *args, **kwargs):
        # Only recruiters can update status
        if request.user.role != 'RECRUITER':
            return Response(
                {"success": False, "message": "Only recruiters can update applications"}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        instance = self.get_object()
        old_status = instance.status
        new_status = request.data.get('status')
        
        if new_status and new_status != old_status:
            # Update status logic
            instance.update_status(new_status, request.data.get('recruiter_notes', ''))
            
            # Record history
            ApplicationStatusHistory.objects.create(
                application=instance,
                old_status=old_status,
                new_status=new_status,
                changed_by=request.user,
                notes=request.data.get('notes', '')
            )
            
        serializer = self.get_serializer(instance)
        return Response({"success": True, "data": serializer.data})
        
    def destroy(self, request, *args, **kwargs):
        # Candidates can withdraw
        instance = self.get_object()
        if request.user.role == 'CANDIDATE':
            instance.status = Application.ApplicationStatus.WITHDRAWN
            instance.save()
            return Response({"success": True, "message": "Application withdrawn"}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)

from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Match
from .serializers import MatchSerializer, MatchListSerializer
from .utils import create_or_update_match
from resumes.models import Resume
from jobs.models import Job

class MatchListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MatchListSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'CANDIDATE':
            return Match.objects.filter(resume__user=user).order_by('-overall_score')
        elif user.role == 'RECRUITER':
            return Match.objects.filter(job__recruiter=user).order_by('-overall_score')
        return Match.objects.none()
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"success": True, "data": serializer.data})

class MatchDetailView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MatchSerializer
    queryset = Match.objects.all()
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Mark as viewed
        if request.user.role == 'CANDIDATE':
            if not instance.is_viewed_by_candidate:
                instance.is_viewed_by_candidate = True
                instance.save()
        elif request.user.role == 'RECRUITER':
            if not instance.is_viewed_by_recruiter:
                instance.is_viewed_by_recruiter = True
                instance.save()
                
        serializer = self.get_serializer(instance)
        return Response({"success": True, "data": serializer.data})

class CalculateMatchView(views.APIView):
    """
    Trigger match calculation manually.
    For candidates: calculates matches against all active jobs.
    For recruiters: calculates matches for a specific job against all active resumes.
    """
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request):
        user = request.user
        matches_created = 0
        
        if user.role == 'CANDIDATE':
            # Get user's active resume (best one)
            resume = Resume.objects.filter(user=user, is_active=True).first()
            if not resume:
                return Response(
                    {"success": False, "message": "No active resume found"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Match against all active jobs
            jobs = Job.objects.filter(status='ACTIVE')
            for job in jobs:
                create_or_update_match(resume, job)
                matches_created += 1
                
        elif user.role == 'RECRUITER':
            job_id = request.data.get('job_id')
            if not job_id:
                return Response(
                    {"success": False, "message": "job_id is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            job = get_object_or_404(Job, id=job_id, recruiter=user)
            
            # Match against all active resumes
            resumes = Resume.objects.filter(is_active=True)
            for resume in resumes:
                create_or_update_match(resume, job)
                matches_created += 1
        
        return Response({
            "success": True, 
            "message": f"Calculated {matches_created} matches"
        })

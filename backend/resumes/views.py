from rest_framework import generics, permissions, status, parsers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Resume
from .serializers import ResumeSerializer, ResumeListSerializer
from .utils import parse_resume, analyze_resume
import os

class ResumeListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ResumeListSerializer
        return ResumeSerializer

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user, is_active=True)

    def create(self, request, *args, **kwargs):
        # Add user to data
        data = request.data.copy()
        
        # Validate file type
        if 'file' in request.FILES:
            file_obj = request.FILES['file']
            ext = os.path.splitext(file_obj.name)[1].lower().replace('.', '')
            if ext not in ['pdf', 'docx']:
                return Response(
                    {"success": False, "message": "Only PDF and DOCX files are allowed"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            data['file_type'] = ext
            data['file_size'] = file_obj.size
            data['title'] = data.get('title', file_obj.name)
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        resume = serializer.save(user=self.request.user)
        
        # Trigger parsing and analysis
        try:
            # Parse text
            text = parse_resume(resume.file.path, resume.file_type)
            resume.parsed_text = text
            resume.is_parsed = True
            
            # Analyze
            scores = analyze_resume(text)
            for key, value in scores.items():
                setattr(resume, key, value)
                
            resume.save()
            
            # Update user's resume score (average of all active resumes or best one)
            # For simplicity, let's take the best score
            best_score = Resume.objects.filter(user=request.user, is_active=True).order_by('-overall_score').first()
            if best_score and hasattr(request.user, 'candidate_profile'):
                profile = request.user.candidate_profile
                profile.resume_score = best_score.overall_score
                profile.save()
                
        except Exception as e:
            print(f"Error processing resume: {e}")
            # Don't fail the request, just log error
        
        # Re-serialize with updated data
        response_serializer = ResumeSerializer(resume)
        headers = self.get_success_headers(response_serializer.data)
        
        return Response(
            {"success": True, "data": response_serializer.data}, 
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

class ResumeDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ResumeSerializer
    
    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user, is_active=True)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
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
        # Soft delete
        instance.is_active = False
        instance.save()
        return Response({"success": True, "message": "Resume deleted successfully"}, status=status.HTTP_200_OK)

class ResumeAnalysisView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, pk):
        resume = get_object_or_404(Resume, pk=pk, user=request.user)
        
        data = {
            "overall_score": resume.overall_score,
            "breakdown": {
                "keywords": resume.keyword_score,
                "format": resume.format_score,
                "experience": resume.experience_score,
                "achievements": resume.achievement_score
            },
            "is_parsed": resume.is_parsed,
            "file_size": resume.file_size,
            "word_count": len(resume.parsed_text.split()) if resume.parsed_text else 0
        }
        
        return Response({"success": True, "data": data})

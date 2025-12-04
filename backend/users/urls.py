from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    RegisterView, 
    UserDetailView, 
    CandidateProfileView, 
    RecruiterProfileView,
    LogoutView,
    EmailTokenObtainPairView
)

urlpatterns = [
    # Auth
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/login/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='auth_logout'),
    
    # User & Profiles
    path('users/me/', UserDetailView.as_view(), name='user_me'),
    path('users/me/candidate-profile/', CandidateProfileView.as_view(), name='candidate_profile'),
    path('users/me/recruiter-profile/', RecruiterProfileView.as_view(), name='recruiter_profile'),
]

from django.urls import path
from .views import MatchListView, MatchDetailView, CalculateMatchView

urlpatterns = [
    path('matches/', MatchListView.as_view(), name='match_list'),
    path('matches/<int:pk>/', MatchDetailView.as_view(), name='match_detail'),
    path('matches/calculate/', CalculateMatchView.as_view(), name='match_calculate'),
]

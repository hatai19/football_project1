from django.urls import path
from .views import MatchList, MatchDetail, ProfileListView,\
    PastMatchListAPIView, JoinMatchAPIView, MatchCommentAPI, ProfileAPIView,UserRegistration, LoginView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView

urlpatterns = [
    path("<int:pk>/", MatchDetail.as_view(), name="match_detail"),
    path("", MatchList.as_view(), name="match_list"),
    path("profiles/", ProfileListView.as_view(), name="profile_list"),
    path("past-matches/", PastMatchListAPIView.as_view(), name="past_matches"),
    path('<int:match_id>/join/', JoinMatchAPIView.as_view(), name='join_match'),
    path('<int:match_id>/comment/',
         MatchCommentAPI.as_view(), name='match_comment'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('registration/', UserRegistration.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

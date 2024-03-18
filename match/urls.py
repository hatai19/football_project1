from django.urls import path
from . import views
from .views import join_match

app_name = 'match'

urlpatterns = [
    path('', views.match_list, name='match_list'),
    path('<int:id>/', views.match_detail, name='match_detail'),
    path('<int:match_id>/comment/',
         views.match_comment, name='match_comment'),
    path('search/', views.match_search, name='match_search'),
    path('<int:match_id>/join/', join_match, name='join_match'),
    path('past-matches/', views.past_matches, name='past_matches'),
    path('profiles/', views.profile_list, name='profile_list'),

]

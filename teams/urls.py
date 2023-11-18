from django.urls import path
from teams.views import TeamView, TeamsView

urlpatterns = [
    path("teams/", TeamsView.as_view()),
    path("teams/<int:team_id>/", TeamView.as_view()),
]
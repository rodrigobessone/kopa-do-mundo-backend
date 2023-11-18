from rest_framework.response import Response
from rest_framework.views import APIView
from django.forms.models import model_to_dict
from teams.models import Team
from utils import data_processing
from exceptions import (
    ImpossibleTitlesError,
    InvalidYearCupError,
    NegativeTitlesError,
)


class TeamsView(APIView):
    def post(self, request):
        payload = request.data
        if payload.get("id"):
            payload.pop("id")
        try:
            data_processing(payload)

            team = Team(**payload)
            team.save()

            return Response(model_to_dict(team), 201)
        except (
            NegativeTitlesError,
            InvalidYearCupError,
            ImpossibleTitlesError,
        ) as err:
            return Response({"error": err.message}, 400)

    def get(self, request):
        data = Team.objects.all()
        data_dict = []

        for element in data:
            e = model_to_dict(element)
            data_dict.append(e)

        return Response(data_dict, 200)


class TeamView(APIView):
    def get(self, request, team_id):
        try:
            team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, 404)

        team_dict = model_to_dict(team)
        return Response(team_dict, 200)

    def patch(self, request, team_id):
        try:
            team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, 404)

        for key, value in request.data.items():
            setattr(team, key, value)
        team.id = team_id
        team.save()

        team_dict = model_to_dict(team)
        return Response(team_dict, 200)

    def delete(self, request, team_id):
        try:
            team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, 404)

        team.delete()
        return Response(status=204)
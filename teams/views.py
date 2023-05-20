from rest_framework.views import APIView, Request, Response, status
from django.forms.models import model_to_dict
from teams.models import Team
from teams.utils import data_processing
from teams.exceptions import \
    NegativeTitlesError, InvalidYearCupError, ImpossibleTitlesError


class TeamView(APIView):
    def post(self, request: Request) -> Response:
        try:
            data_processing(request.data)
        except (
            NegativeTitlesError,
            InvalidYearCupError,
            ImpossibleTitlesError
        ) as error:
            return Response(
                {"error": error.args[0]},
                status.HTTP_400_BAD_REQUEST
            )

        return Response(
            model_to_dict(Team.objects.create(**request.data)),
            status.HTTP_201_CREATED
        )

    def get(self, request: Request) -> Response:
        return Response(
            (model_to_dict(team) for team in Team.objects.all()),
            status.HTTP_200_OK
        )


class TeamDetailView(APIView):
    def get(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"},
                status.HTTP_404_NOT_FOUND
            )

        return Response(model_to_dict(team), status.HTTP_200_OK)

    def patch(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"},
                status.HTTP_404_NOT_FOUND
            )

        for key, value in request.data.items():
            setattr(team, key, value)

        team.save()

        return Response(model_to_dict(team), status.HTTP_200_OK)

    def delete(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"},
                status.HTTP_404_NOT_FOUND
            )

        team.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

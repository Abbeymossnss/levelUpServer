from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, GameType, Gamer

class GameView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type"""
        game = Game.objects.get(pk=pk)
        serializer = GameSerializer(game)
    
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all game types    """
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        """Returns: Response -- JSON serialized list of game types
        """
        return Response(serializer.data)
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        game_type = GameType.objects.get(pk=request.data["game_type"])

        game = Game.objects.create(
            title=request.data["title"],
            maker=request.data["maker"],
            num_of_players=request.data["num_of_players"],
            skill_level=request.data["skill_level"],
            gamer=gamer,
            game_type=game_type
        )
        serializer = GameSerializer(game)
        return Response(serializer.data)
class GameTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameType
        fields = ('id', 'label', 'description', )
class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    game_type = GameTypeSerializer(many=False)

    class Meta:
        model = Game
        fields = ('id', 'title', 'maker', 'game_type', 'num_of_players', 'skill_level',)

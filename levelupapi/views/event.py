from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game, GameType

class EventView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type"""
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
    
        return Response(serializer.data)

    def list(self, request):
        game_to_filter_by = request.query_params.get('game')

        if game_to_filter_by:
            events = Event.objects.filter(game=game_to_filter_by)
        else:
            events = Event.objects.all()

        serializer = EventSerializer(events, many=True)
        """Returns: Response -- JSON serialized list of game types
        """
    

        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        organizer = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data["game"])
        game_type = GameType.objects.get(pk=request.data["game_type"])

        event = Event.objects.create(
            date=request.data["date"],
            organizer=organizer,
            game= game,
            game_type=game_type
        )
        serializer = EventSerializer(event)
        return Response(serializer.data)

class GamerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gamer
        fields = ('id','user', 'bio', 'full_name', )

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ( 'id', 'title', 'maker', 'num_of_players', 'skill_level', )

class GameTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameType
        fields = ('id','label', 'description', )


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    organizer = GamerSerializer(many=False)
    attendees = GamerSerializer(many=True)
    game = GameSerializer(many=False)
    game_type = GameTypeSerializer(many=False)

    class Meta:
        model = Event
        fields = ('id', 'organizer', 'date', 'game', 'game_type', 'attendees',)
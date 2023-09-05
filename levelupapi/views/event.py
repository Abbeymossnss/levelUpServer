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


        event = Event.objects.create(
            date=request.data["date"],
            organizer=organizer,
            game=game,

        )
        serializer = EventSerializer(event)
        return Response(serializer.data)
    
    def update(self, request, pk):
    # """Handle PUT requests for a game

    # Returns:
    #     Response -- Empty body with 204 status code
    # """

        event = Event.objects.get(pk=pk)
        event.date = request.data["date"]

        gamer = Gamer.objects.get(pk=request.data["organizer"])
        event.organizer = gamer

        

        game = Game.objects.get(pk=request.data["game"])
        event.game = game
        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)



class GamerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gamer
        fields = ('id', 'user', 'bio', 'full_name', )


class GameTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameType
        fields = ('id', 'label', 'description', )


class GameSerializer(serializers.ModelSerializer):
    game_type = GameTypeSerializer(many=False)

    class Meta:
        model = Game
        fields = ('id', 'title', 'maker', 'num_of_players',
                  'skill_level', 'game_type')


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    organizer = GamerSerializer(many=False)
    attendees = GamerSerializer(many=True)
    game = GameSerializer(many=False)

    class Meta:
        model = Event
        fields = ('id', 'organizer', 'date', 'game', 'attendees',)

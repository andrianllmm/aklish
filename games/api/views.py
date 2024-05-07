from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import GameStats
from .serializers import GameStatsSerializer


class GameStatsAPIView(APIView):
    permission_classes = [AllowAny]


    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"error": "User not authenticated"}, status=status.HTTP_403_FORBIDDEN)

        user = request.user
        queryset = GameStats.objects.filter(user=user)
        serializer = GameStatsSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"error": "User not authenticated"}, status=status.HTTP_403_FORBIDDEN)

        user = request.user
        game_stats = GameStats.objects.get_or_create(user=user)[0]
        
        won = request.data.get("won")
        solution = request.data.get("solution")
        lang = request.data.get("lang")
        
        if won is not None and solution is not None and lang is not None:
            game_stats.update_stats(won, solution, lang)
            serializer = GameStatsSerializer(game_stats)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)

from django.http.response import Http404
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated

from core.general.utils.responses import *

from .models import Favorite
from .serializers import FavoriteSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        favorites = Favorite.objects.filter(owner=request.user)
        serializer = FavoriteSerializer(favorites, many=True)
        return success_response(key="favorites", data=serializer.data)

    def retrieve(self, request, pk=None):
        try:
            favorite = self.get_object()

            if favorite.owner == request.user:
                serializer = FavoriteSerializer(favorite)
                return success_response(key="favorite", data=serializer.data)

            return fail_response(
                errors={"user": "You are not Favorite Owner"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except Http404:
            return error_response("Favorite not found")

    def create(self, request):
        serializer = FavoriteSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get("owner")
            if user != None and user == request.user:
                serializer.save()
                return success_response(key="favorite", data=serializer.data)
            return fail_response(
                {"user": "You are not Favorite Owner"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return fail_response(serializer.errors)

    def update(self, request, pk=None):
        try:
            favorite = self.get_object()
        except Http404:
            return error_response("Favorite not found")

        serializer = FavoriteSerializer(favorite, data=request.data)

        if serializer.is_valid():
            if favorite.owner == request.user:
                serializer.save()
                return success_response(key="favorite", data=serializer.data)

            return fail_response(
                {"user": "You are not Favorite Owner"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return fail_response(serializer.errors)

    def destroy(self, request, pk=None):
        try:
            favorite = self.get_object()
            if favorite.owner == request.user:
                favorite.delete()
                return success_response()

            return fail_response(
                {"user": "You are not Favorite Owner"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except Http404:
            return error_response("Favorite not found")

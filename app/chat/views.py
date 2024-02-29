from django.shortcuts import render
from .serializers import InAppChatSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework import generics, status, viewsets, filters
from .models import InAppChat
from rest_framework.decorators import action


# def index(request):
#     return render(request, "chat/index.html")


# def room(request, room_name):
#     return render(request, "chat/room.html", {"room_name": room_name})


class InAppChatViewSets(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = InAppChatSerializer
    permission_classes = [IsAuthenticated]
    queryset = InAppChat.objects.all()

    def paginate_results(self, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=['POST'],
        detail=True,
        serializer_class=None,
        url_path='confirm-read-recipient',
    )
    def confirm_read_recipient(self, request, pk=None):
        """to confirm that  the message read reciept"""
        chat = self.get_object()

        if chat:
            chat.is_read = True
            chat.save()
            return Response(
                {"success": True, "message": "Chat recipient updated successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"success": False, "message": "Chat not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

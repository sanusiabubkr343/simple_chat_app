from rest_framework import serializers

from .models import InAppChat


class InAppChatSerializer(serializers.ModelSerializer):
    sender_username = serializers.StringRelatedField(source='sender.sender_username')
    receiver_username = serializers.StringRelatedField(source='receiver.sender_username')

    class Meta:
        model = InAppChat
        fields = "__all__"

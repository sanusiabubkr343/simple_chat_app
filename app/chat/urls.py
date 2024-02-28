from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InAppChatViewSets, index, room

app_name = 'chat'

router = DefaultRouter()
router.register('', InAppChatViewSets)


urlpatterns = [
    path('interfaces/', include(router.urls)),
    path("", index, name="index"),
    path("<str:room_name>/", room, name="room"),
]

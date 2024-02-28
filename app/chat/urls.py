from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InAppChatViewSets

app_name = 'chat'

router = DefaultRouter()
router.register('', InAppChatViewSets)


urlpatterns = [
    path('', include(router.urls)),
]

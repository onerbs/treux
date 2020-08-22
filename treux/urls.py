from django.urls import path, include
from rest_framework.routers import DefaultRouter

from cards.views import ListViewSet, CardViewSet
from teams.views import TeamViewSet
from users.views import UserViewSet
from boards.views import BoardViewSet
from comments.views import CommentViewSet

router = DefaultRouter()
router.register('cards', CardViewSet)
router.register('lists', ListViewSet)
router.register('teams', TeamViewSet)
router.register('users', UserViewSet)
router.register('boards', BoardViewSet)
router.register('comments', CommentViewSet)

api_root = 'api/v1/'
urlpatterns = [
	path(api_root, include(router.urls)),
	path(api_root, include('core.urls')),
]

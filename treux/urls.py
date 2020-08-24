from rest_framework.routers import DefaultRouter

from cards.views import ListViewSet, CardViewSet
from teams.views import TeamViewSet
from users.views import UserViewSet
from boards.views import BoardViewSet
from comments.views import CommentViewSet
from treux.api import api_urls

router = DefaultRouter()
router.register('cards', CardViewSet)
router.register('lists', ListViewSet)
router.register('teams', TeamViewSet)
router.register('users', UserViewSet)
router.register('boards', BoardViewSet)
router.register('comments', CommentViewSet)

urlpatterns = api_urls([router.urls, 'core.urls'])

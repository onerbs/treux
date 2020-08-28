from rest_framework.routers import SimpleRouter

from teams.views import TeamViewSet
from users.views import UserViewSet
from boards.views import BoardViewSet
from cards.views import ListViewSet, CardViewSet
from comments.views import CommentViewSet
from core.api import api_patterns

router = SimpleRouter()
router.register('teams', TeamViewSet)
router.register('users', UserViewSet)
router.register('boards', BoardViewSet)
router.register('lists', ListViewSet)
router.register('cards', CardViewSet)
router.register('comments', CommentViewSet)

urlpatterns = api_patterns([router.urls, 'core.urls'])

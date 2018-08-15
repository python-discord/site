from rest_framework.routers import SimpleRouter

from .viewsets import SnakeNameViewSet


# http://www.django-rest-framework.org/api-guide/routers/#simplerouter
router = SimpleRouter(trailing_slash=False)
router.register(r'snake-names', SnakeNameViewSet)

app_name = 'api'
urlpatterns = router.urls

from django.conf.urls import include, url
from django.conf import settings
from rest_framework import routers
from .views import (UserViewSet, GroupViewSet, GoalViewSet, TaskViewSet,
    TaskActionViewSet)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'goals', GoalViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'task_actions', TaskActionViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'auth/', include('rest_auth.urls')),
    url(r'auth/registration/', include('rest_auth.registration.urls'))
]

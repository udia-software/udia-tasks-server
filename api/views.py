"""
Views for API
"""
from api.models import Goal, Task, TaskAction
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import (UserSerializer, GroupSerializer, GoalSerializer,
    TaskSerializer, TaskActionSerializer)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    queryset = Goal.objects.all()

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskActionViewSet(viewsets.ModelViewSet):
    queryset = TaskAction.objects.all()
    serializer_class = TaskActionSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(),]
        else:
            return [IsAdminUser(),]

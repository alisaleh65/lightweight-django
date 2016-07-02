from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import authentication, permissions, viewsets

from .model import Sprint
from .serializers import SprintSerializer, TaskSerializer, UserSerializer

User = get_user_model()

class TaskViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing and creating tasks."""
    
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class UserViewSet(DefaultsMixin, viewsets.ReadOnlyModelViewSet):
    """API endpoint for listing users."""
    
    lookup_field = User.USER_NAME_FIELD
    lookup_url_kwarg = User.USER_NAME_FIELD
    queryset = User.objects.order_by(User.USER_NAME_FIELD)
    serializer_class = UserSerializer
    
class DefaultsMixin:
    """Default settings for view authentication, permissions, filtering and pagination."""
    
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = (
        permissions.IsAuthenticated,
    )
    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100

class SprintViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing and creating sprints."""
    
    queryset = Sprint.objects.order_by('end')
    serializer_class = SprintSerializer

# Create your views here.

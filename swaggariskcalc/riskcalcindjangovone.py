from rest_framework import serializers, viewsets, status, routers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.urls import path, include
from django.conf.urls import url
from django.apps import AppConfig
from django.apps.registry import apps

# Define a serializer for the Project model
class ProjectSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    dependencies = serializers.ListField(child=serializers.CharField(), required=False)

# Define the Project model
class Project:
    def __init__(self, id, name, description, dependencies=None):
        self.id = id
        self.name = name
        self.description = description
        self.dependencies = dependencies or []

# Define a viewset for projects
class ProjectViewSet(viewsets.ViewSet):
    def list(self, request):
        projects = list(apps.get_app_config('api').projects.values())
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            project_id = f'PN-{len(apps.get_app_config("api").projects) + 1:05d}'
            project = Project(project_id, **serializer.validated_data)
            apps.get_app_config('api').projects[project_id] = project
            return Response({"message": "Project created successfully", "project_id": project_id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        project = apps.get_app_config('api').projects.get(pk)
        if not project:
            raise Http404
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def dependencies(self, request, pk=None):
        project = apps.get_app_config('api').projects.get(pk)
        if not project:
            raise Http404
        dependencies = [apps.get_app_config('api').projects.get(dep_id) for dep_id in project.dependencies]
        serializer = ProjectSerializer(dependencies, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_dependency(self, request, pk=None):
        project = apps.get_app_config('api').projects.get(pk)
        if not project:
            raise Http404
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            dependency_id = serializer.validated_data.get('id')
            if dependency_id not in apps.get_app_config('api').projects:
                return Response({"message": "Dependency project not found"}, status=status.HTTP_400_BAD_REQUEST)
            if dependency_id not in project.dependencies:
                project.dependencies.append(dependency_id)
                return Response({"message": "Dependency added successfully"})
            return Response({"message": "Dependency already exists"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create a Django app configuration
class ApiConfig(AppConfig):
    name = 'api'

# Define project data storage in the app configuration
ApiConfig.projects = {}

# Define Django REST framework viewset and URL patterns
router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)

# Django app URLs
urlpatterns = [
    path('', include(router.urls)),
]

# To run the Django development server, you can use 'python manage.py runserver'

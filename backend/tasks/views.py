from rest_framework import viewsets, permissions, status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django.db import models
from django.contrib.auth.models import User

from .models import Task
from .serializers import TaskSerializer, RegisterSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(
            models.Q(created_by=self.request.user) | models.Q(shared_with=self.request.user)
        ).distinct()

    def perform_create(self, serializer):
        task = serializer.save(created_by=self.request.user)
        # Evitar que se comparta consigo mismo
        if task.shared_with.filter(id=self.request.user.id).exists():
            task.shared_with.remove(self.request.user)

    def perform_update(self, serializer):
        task = serializer.save(created_by=self.request.user)
        if task.shared_with.filter(id=self.request.user.id).exists():
            task.shared_with.remove(self.request.user)


class RegisterView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Usuario creado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

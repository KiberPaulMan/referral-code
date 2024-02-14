from rest_framework import permissions, generics, status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile
from .serializers import (
    ProfileSerializer,
    ProfileCodeSerializer,
    ProfileCreateSerializer
)


class ProfileAPIView(generics.RetrieveAPIView):
    """
    API для просмотра информации о пользователе и его рефералах
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProfileCodeAPIView(APIView):
    """
    API для создания и удаления реферального кода
    """
    def get_object(self, pk):
        return Profile.objects.get(pk=pk)

    def patch(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileCodeSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        profile = self.get_object(pk)
        profile.ref_code = ""
        profile.end_date_code = None
        profile.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileCreateAPIView(CreateAPIView):
    """
    API для регистрации пользователя тремя способами:
        1. Обычная регистрация
        2. Регистрация по реферальному коду
        3. Регистрация по email реферера
    """
    queryset = Profile.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ProfileCreateSerializer

    def get_serializer_context(self):
        context = {'request': self.request}
        if 'uuid' in self.kwargs:
            context['uuid'] = self.kwargs['uuid']
        return context

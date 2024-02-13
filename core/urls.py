from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/profile/register/', views.ProfileCreateAPIView.as_view()),
    path('api/v1/profile/register/<str:uuid>/', views.ProfileCreateAPIView.as_view()),

    path('api/v1/profile/<int:pk>/', views.ProfileAPIView.as_view()),
    path('api/v1/profile/<int:pk>/code/', views.ProfileCodeAPIView.as_view()),
]

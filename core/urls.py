from django.urls import include, path
from . import views

temp_url = "http://127.0.0.1:8000/reg/5j5cxcuPZ6",

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('reg/<str:uuid>/', views.register_user, name='referral-register'),
    path('email-register/', views.register_by_email, name='register-by-email'),

    path('profile/<int:pk>/', views.ProfileAPIView.as_view(), name='user-detail'),
    path('profile/<int:pk>/code/', views.ProfileCodeAPIView.as_view(), name='update-or-delete-code'),
]

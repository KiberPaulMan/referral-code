from django.shortcuts import render, redirect
from rest_framework import permissions, generics, status
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from .forms import SignUpForm, EmailForm
from .models import Profile
from .serializers import ProfileSerializer, ProfileCodeSerializer


def register_user(request, uuid=None):
    """
    Регистрация пользователя с реферальным кодом и без него
    :param request:
    :param uuid:
    :return:
    """
    if request.method == 'POST':
        user_form = SignUpForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()

            if uuid:
                try:
                    referrer = Profile.objects.get(ref_code=settings.URL_REF_CODE + uuid)
                    Profile.objects.create(user=user, referrer=referrer.user)
                except Profile.DoesNotExist:
                    user.delete()
                    return HttpResponse('Incorrect referral code link')

            elif 'email' in request.session:
                referrer = Profile.objects.get(user__email=request.session.get('email'))
                Profile.objects.create(user=user, referrer=referrer.user)

            else:
                Profile.objects.create(user=user)

            return redirect('user-detail', pk=Profile.objects.last().id)
    else:
        user_form = SignUpForm()
    return render(request, 'core/register.html', {'form': user_form})


def register_by_email(request):
    """
    Регистрация пользователя через email реферера
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = EmailForm(request.POST)

        if form.is_valid():
            referrer_email = form.cleaned_data.get('email')
            try:
                Profile.objects.get(user__email=referrer_email)
                request.session['email'] = referrer_email
                return redirect('register')
            except Profile.DoesNotExist:
                return HttpResponse('Incorrect referrer email')

    else:
        form = EmailForm()
    return render(request, 'core/register.html', {'form': form})


class ProfileAPIView(generics.RetrieveAPIView):
    """
    APi для просмотра информации о пользователе и его рефералах
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
            return JsonResponse(status=status.HTTP_201_CREATED, data=serializer.data)
        return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data="wrong parameters")

    def delete(self, request, pk):
        profile = self.get_object(pk)
        profile.ref_code = ""
        profile.end_date_code = None
        profile.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

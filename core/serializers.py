from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile
from rest_framework.exceptions import ValidationError


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    referrals = serializers.SerializerMethodField(read_only=True)
    referrer_username = serializers.CharField(source='referrer.username', read_only=True, default='')
    referrer_email = serializers.EmailField(source='referrer.email', read_only=True, default='')

    class Meta:
        model = Profile
        exclude = ['user', 'referrer']

    def get_referrals(self, obj):
        queryset = Profile.objects.filter(referrer=obj.user)
        return ReferralSerializer(queryset, many=True).data


class ReferralSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = Profile
        fields = ('id', 'username', 'email')


class ProfileCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('ref_code', 'end_date_code',)

    def update(self, instance, validated_data):
        instance.ref_code = Profile.get_ref_code()
        return super().update(instance, validated_data)


class ProfileCreateSerializer(serializers.ModelSerializer):
    def validate(self, data):
        user_email = data['user']['email']
        if user_email and Profile.objects.filter(user__email=user_email).exists():
            raise ValidationError("A user with this email already exists!")
        return data

    username = serializers.CharField(source='user.username')
    password = serializers.CharField(source='user.password')
    email = serializers.EmailField(source='user.email')
    referrer_email = serializers.EmailField(required=False)

    class Meta:
        model = Profile
        fields = ('username', 'email', 'password', 'referrer_email')

    def create(self, validated_data):
        referrer_email = validated_data.get('referrer_email', None)

        try:
            user = self.create_user(validated_data)
        except:
            raise ValidationError('This user already exists!')

        if 'uuid' in self.context:
            try:
                referrer = Profile.objects.get(ref_code=settings.URL_REF_CODE + self.context['uuid'])
                profile = Profile.objects.create(user=user, referrer=referrer.user)
            except Profile.DoesNotExist:
                user.delete()
                raise APIException('Incorrect referral code link!')

        elif referrer_email:
            try:
                referrer = Profile.objects.get(user__email=referrer_email)
                profile = Profile.objects.create(user=user, referrer=referrer.user)
            except Profile.DoesNotExist:
                user.delete()
                raise ValidationError('Incorrect referrer email!')

        else:
            profile = Profile.objects.create(user=user)
        return profile

    @staticmethod
    def create_user(validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(
            username=user_data['username'],
            email=user_data['email']
        )
        user.set_password(user_data['password'])
        user.save()
        return user

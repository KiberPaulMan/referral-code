from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    referrals = serializers.SerializerMethodField(read_only=True)
    referrer_username = serializers.CharField(source='referrer.username', read_only=True)
    referrer_email = serializers.EmailField(source='referrer.email', read_only=True)

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
        fields = ('ref_code', 'end_date_code', )

    def update(self, instance, validated_data):
        instance.ref_code = Profile.get_ref_code()
        return super().update(instance, validated_data)

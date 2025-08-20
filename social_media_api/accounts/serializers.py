from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required = False)
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'bio', 'profile_pic' 'password')


    def create(self, validated_data):
        user  = CustomUser(
            username = validated_data['username'],
            email = validated_data['email'],
            bio = validated_data['bio', ''],
            profile_pic = validated_data['profile_pic', None]
        )

        user.set_password(validated_data['password'])
        user.save()
        return user


    def update(self, instance, validated_data):

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)

        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


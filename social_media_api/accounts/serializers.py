from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    # Specify the password field explicitly as CharField (since it's required)
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'bio', 'profile_pic', 'password')


    def create(self, validated_data):
        # Use get_user_model().objects.create_user for better compatibility
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.bio = validated_data.get('bio', '')
        user.profile_pic = validated_data.get('profile_pic', None)
        user.save()

        # Create a token for the user
        Token.objects.create(user=user)
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)

        # Handle password update
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        instance.save()
        return instance
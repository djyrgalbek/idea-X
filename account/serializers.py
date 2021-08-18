from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import IdeaUser
from .utils import send_activation_code


class RegisterSerializers(serializers.ModelSerializer):
    password = serializers.CharField(min_length=4, write_only=True)
    password_confirm = serializers.CharField(min_length=4, write_only=True)

    class Meta:
        model = IdeaUser
        fields = ('email', 'password', 'password_confirm')

    def validate(self, validated_data):
        password = validated_data.get('password')
        password_confirm = validated_data.get('password_confirm')

        if password != password_confirm:
            raise serializers.ValidationError('Пароли не совпадают!')
        return validated_data

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = IdeaUser.objects.create_user(email=email, password=password)
        send_activation_code(email=user.email, activation_code=user.activation_code)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        label='Password',
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            if not user:
                message = 'Такого юзера не существует!'
                raise serializers.ValidationError(message, code='authorization')
        else:
            message = 'Введите логин или пароль!'
            raise serializers.ValueError(message, code='authorization')

        attrs['user'] = user
        return attrs

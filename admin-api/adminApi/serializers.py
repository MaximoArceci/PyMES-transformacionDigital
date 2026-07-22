from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Pyme


class PymeSerializer(serializers.ModelSerializer):
    maturity_level = serializers.IntegerField(read_only=True)
    maturity_band = serializers.CharField(read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Pyme
        fields = (
            "id",
            "name",
            "legal_name",
            "address",
            "locality",
            "province",
            "tax_id",
            "website",
            "description",
            "work_type",
            "enterprise_type",
            "sector",
            "maturity_score",
            "maturity_level",
            "maturity_band",
            "rating",
            "latitud",
            "longitud",
        )


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        email = value.strip().lower()
        if get_user_model().objects.filter(username__iexact=email).exists():
            raise serializers.ValidationError("Ya existe una cuenta con este correo.")
        return email

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        email = validated_data["email"]
        return get_user_model().objects.create_user(
            username=email, email=email, password=validated_data["password"]
        )


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(write_only=True)
    username_field = "email"

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        return token

    def validate(self, attrs):
        self.user = authenticate(
            request=self.context.get("request"),
            username=attrs.get("email", "").strip().lower(),
            password=attrs.get("password"),
        )
        if not self.user or not self.user.is_active:
            raise AuthenticationFailed("No existe una cuenta activa con esas credenciales.")
        refresh = self.get_token(self.user)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

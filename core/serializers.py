from django.forms import ValidationError
from rest_framework import serializers

from .models import Banco, Cliente, Credito


class BancoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banco
        fields = "__all__"

    def to_simple(self, instance):
        return {
            "id": instance.id,
            "nombre": instance.nombre,
            "tipo": instance.get_tipo_display(),
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["tipo"] = instance.get_tipo_display()
        return data


class ClienteSerializer(serializers.ModelSerializer):
    edad = serializers.ReadOnlyField()

    class Meta:
        model = Cliente
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["banco"] = BancoSerializer().to_simple(instance.banco)  # pyright: ignore
        data["tipo_persona"] = instance.get_tipo_persona_display()
        return data

    def to_simple(self, instance):
        return {
            "id": instance.id,
            "nombre_completo": instance.nombre_completo,
            "tipo_persona": instance.get_tipo_persona_display(),
        }


class CreditoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Credito
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["banco"] = BancoSerializer().to_simple(instance.banco)  # pyright: ignore
        data["cliente"] = ClienteSerializer().to_simple(instance.cliente)  # pyright: ignore
        data["tipo_credito"] = instance.get_tipo_credito_display()
        return data

    def validate(self, attrs):
        instance = Credito(**attrs)

        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        return attrs

from datetime import date

import django_filters
from django.db.models import Q

from .models import Banco, Cliente, Credito


class ClienteFilter(django_filters.FilterSet):
    nombre_completo = django_filters.CharFilter(lookup_expr="icontains")
    email = django_filters.CharFilter(lookup_expr="icontains")
    nacionalidad = django_filters.CharFilter(lookup_expr="icontains")

    tipo_persona = django_filters.ChoiceFilter(choices=Cliente.TipoPersona.choices)
    banco = django_filters.ModelChoiceFilter(queryset=Banco.objects.all())

    edad_mayor_a = django_filters.NumberFilter(method="filter_edad_min", label="Edad mayor o igual a")
    edad_menor_a = django_filters.NumberFilter(method="filter_edad_max", label="Edad menor o igual a")

    class Meta:
        model = Cliente
        fields = ["tipo_persona", "banco", "nacionalidad"]

    def filter_edad_min(self, queryset, name, value):
        limit_date = date.today().replace(year=date.today().year - int(value))
        return queryset.filter(fecha_de_nacimiento__lte=limit_date)

    def filter_edad_max(self, queryset, name, value):
        limit_date = date.today().replace(year=date.today().year - int(value))
        return queryset.filter(fecha_de_nacimiento__gte=limit_date)


class BancoFilter(django_filters.FilterSet):
    tipo = django_filters.ChoiceFilter(choices=Banco.Tipo.choices)

    class Meta:
        model = Banco
        fields = ["tipo"]


class CreditoFilter(django_filters.FilterSet):
    pago_minimo_mayor_a = django_filters.NumberFilter(field_name="pago_minimo", lookup_expr="gte")
    pago_minimo_menor_a = django_filters.NumberFilter(field_name="pago_minimo", lookup_expr="lte")

    pago_maximo_mayor_a = django_filters.NumberFilter(field_name="pago_maximo", lookup_expr="gte")
    pago_maximo_menor_a = django_filters.NumberFilter(field_name="pago_maximo", lookup_expr="lte")

    plazo_mayor_a = django_filters.NumberFilter(field_name="plazo_meses", lookup_expr="gte")
    plazo_menor_a = django_filters.NumberFilter(field_name="plazo_meses", lookup_expr="lte")

    tipo_credito = django_filters.ChoiceFilter(choices=Credito.TipoCredito.choices)

    cliente = django_filters.ModelChoiceFilter(queryset=Cliente.objects.all())
    banco = django_filters.ModelChoiceFilter(queryset=Banco.objects.all())

    descripcion = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Credito
        fields = ["tipo_credito", "cliente", "banco", "plazo_meses"]

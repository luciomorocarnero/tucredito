from django.shortcuts import redirect, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, views, viewsets

from .filters import ClienteFilter, BancoFilter, CreditoFilter # pyright: ignore
from .models import Banco, Cliente, Credito
from .serializers import BancoSerializer, ClienteSerializer, CreditoSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.select_related("banco").all()
    serializer_class = ClienteSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = ClienteFilter

    search_fields = ["nombre_completo", "email", "telefono"]

    ordering_fields = ["nombre_completo", "fecha_de_nacimiento", "created_at"]
    ordering = ["-created_at"]


class BancoViewSet(viewsets.ModelViewSet):
    queryset = Banco.objects.all()
    serializer_class = BancoSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = BancoFilter

    search_fields = ["nombre"]

    ordering_fields = ["nombre"]
    ordering = ["nombre"]


class CreditoViewSet(viewsets.ModelViewSet):
    queryset = Credito.objects.select_related("cliente", "banco").all()
    serializer_class = CreditoSerializer
    filterset_class = CreditoFilter

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = ["descripcion"]

    ordering_fields = ["created_at"]
    ordering = ["-created_at"]




def creditos_notif(request):
    return render(request, "core/websockets/creditos.html")

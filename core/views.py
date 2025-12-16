from django.shortcuts import render, redirect
from rest_framework import status, views, viewsets
from .models import Cliente, Banco, Credito
from .serializers import ClienteSerializer, BancoSerializer, CreditoSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.select_related("banco").all()
    serializer_class = ClienteSerializer

class BancoViewSet(viewsets.ModelViewSet):
    queryset = Banco.objects.all()
    serializer_class = BancoSerializer

class CreditoViewSet(viewsets.ModelViewSet):
    queryset = Credito.objects.select_related('cliente', 'banco').all()
    serializer_class = CreditoSerializer

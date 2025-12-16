
from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"clientes", views.ClienteViewSet, basename="clientes")
router.register(r"bancos", views.BancoViewSet, basename="bancos")
router.register(r"creditos", views.CreditoViewSet, basename="creditos")


urlpatterns = [
    path("", include(router.urls)),
]

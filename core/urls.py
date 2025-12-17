from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"clientes", views.ClienteViewSet, basename="clientes")
router.register(r"bancos", views.BancoViewSet, basename="bancos")
router.register(r"creditos", views.CreditoViewSet, basename="creditos")

urlpatterns = [
    path("", include(router.urls)),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    path("schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("debug/creditos/", views.creditos_notif, name="creditos_notif"),
]

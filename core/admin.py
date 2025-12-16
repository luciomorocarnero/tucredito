from django.contrib import admin

from .models import Banco, Cliente, Credito


@admin.register(Banco)
class BancoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo", "direccion")
    list_filter = ("tipo",)
    search_fields = ("nombre", "direccion")
    ordering = ("nombre",)

    readonly_fields = ("created_at", "updated_at")


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        "nombre_completo",
        "email",
        "telefono",
        "banco",
        "tipo_persona",
        "created_at",
    )

    search_fields = (
        "nombre_completo",
        "email",
        "telefono",
        "banco__nombre",
    )

    list_filter = ("tipo_persona", "banco")

    ordering = ("nombre_completo",)

    readonly_fields = ("created_at", "updated_at",)

@admin.register(Credito)
class CreditoAdmin(admin.ModelAdmin):
    list_display = (
        "cliente__nombre_completo",
        "banco__nombre",
        "tipo_credito",
        "pago_minimo",
        "pago_maximo",
        "plazo_meses",
        "created_at",
    )

    list_filter = ("tipo_credito", "banco")

    search_fields = (
        "cliente__nombre_completo",
        "banco__nombre",
        "descripcion",
    )

    ordering = ("-created_at",)

    readonly_fields = ("created_at", "updated_at")

    autocomplete_fields = ("cliente", "banco")

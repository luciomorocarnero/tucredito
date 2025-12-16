import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Banco, Cliente, Credito

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Cliente)
def log_cliente_change(sender, instance, created, **kwargs):
    if created:
        logger.info(
            f"CREACION_MODELO | Cliente: ID={instance.pk} | Nombre='{instance.nombre_completo}' | Banco='{instance.banco.nombre}'"
        )
    else:
        logger.info(
            f"ACTUALIZACION_MODELO | Cliente: ID={instance.pk} | Nombre='{instance.nombre_completo}' | Banco='{instance.banco.nombre}'"
        )


@receiver(post_save, sender=Credito)
def log_credito_change(sender, instance, created, **kwargs):
    if created:
        logger.info(
            f"CREACION_MODELO | Credito: ID={instance.pk} | Tipo='{instance.get_tipo_credito_display()}' | Cliente='{instance.cliente.nombre_completo}'"
        )
    else:
        logger.info(f"ACTUALIZACION_MODELO | Credito: ID={instance.pk} | Tipo='{instance.get_tipo_credito_display()}'")


@receiver(post_save, sender=Banco)
def log_banco_change(sender, instance, created, **kwargs):
    if created:
        logger.info(f"CREACION_MODELO | Banco: ID={instance.pk} | Nombre='{instance.nombre}'")
    else:
        logger.info(f"ACTUALIZACION_MODELO | Banco: ID={instance.pk} | Nombre='{instance.nombre}'")

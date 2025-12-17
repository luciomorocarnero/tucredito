import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Banco, Cliente, Credito
from .serializers import CreditoSerializer

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Cliente)
def cliente_change(sender, instance, created, **kwargs):
    if created:
        logger.info(
            f"CREACION_MODELO | Cliente: ID={instance.pk} | Nombre='{instance.nombre_completo}' | Banco='{instance.banco.nombre}'"
        )
    else:
        logger.info(
            f"ACTUALIZACION_MODELO | Cliente: ID={instance.pk} | Nombre='{instance.nombre_completo}' | Banco='{instance.banco.nombre}'"
        )


@receiver(post_save, sender=Credito)
def credito_change(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    group_name = "credito"
    serializer = CreditoSerializer(instance)

    if created:
        logger.info(f"CREACION_MODELO | Credito: ID={instance.pk} | Cliente='{instance.cliente.nombre_completo}'")
        message = {
            "type": "credito.change",
            "payload": {
                "type": "credito.add",
                "data": serializer.data,
            },
        }
    else:
        message = {
            "type": "credito.change",
            "payload": {
                "type": "credito.update",
                "data": serializer.data,
            },
        }
        logger.info(f"ACTUALIZACION_MODELO | Credito: ID={instance.pk} | Cliente='{instance.cliente.nombre_completo}'")

    async_to_sync(channel_layer.group_send)(group_name, message)  # pyright: ignore


@receiver(post_delete, sender=Credito)
def credito_delete(sender, instance, **kwargs):
    logger.info(f"ELIMINACION_MODELO | Credito: ID={instance.pk} | Cliente='{instance.cliente.nombre_completo}'")

    channel_layer = get_channel_layer()
    group_name = "credito"
    serializer = CreditoSerializer(instance)

    message = {
        "type": "credito.delete",
        "payload": {
            "type": "credito.delete",
            "data": serializer.data,
        },
    }

    async_to_sync(channel_layer.group_send)(group_name, message)  # pyright: ignore


@receiver(post_save, sender=Banco)
def banco_change(sender, instance, created, **kwargs):
    if created:
        logger.info(f"CREACION_MODELO | Banco: ID={instance.pk} | Nombre='{instance.nombre}'")
    else:
        logger.info(f"ACTUALIZACION_MODELO | Banco: ID={instance.pk} | Nombre='{instance.nombre}'")


@receiver(post_save, sender=Credito)
def mail_credito_create(sender, instance, created, **kwargs):
    if created and settings.EMAIL_AVAILABLE:
        try:
            cliente_mail = instance.cliente.email

            if cliente_mail:
                subject = f"Nuevo credito aprobado"
                message = (
                    f"Hola {instance.cliente.nombre_completo},\n\n"
                    f"Te informamos que se ha registrado un nuevo credito bajo tu nombre.\n\n"
                    f"{instance.descripcion}\n\n"
                    f"Tipo de credito: {instance.get_tipo_credito_display()}\n"
                    f"Banco: {instance.banco.nombre}\n"
                    f"Plazo en meses: {instance.plazo_meses}\n"
                    f"ID de operacion: {instance.pk}\n"
                    f"ID de operacion: {instance.pk}\n"
                )

                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [cliente_mail],
                    fail_silently=False,
                )
                logger.info(f"EMAIL_ENVIADO | Credito ID={instance.pk} enviado a {cliente_mail}")
            else:
                logger.warning(f"EMAIL_NO_ENVIADO | El cliente ID={instance.cliente.pk} no tiene email registrado.")

        except Exception as e:
            logger.error(f"ERROR_ENVIO_EMAIL | Credito ID={instance.pk}: {str(e)}")

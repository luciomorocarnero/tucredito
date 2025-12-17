import pytest
from django.core import mail
from django.core.mail import send_mail
from django.conf import settings 

@pytest.mark.django_db
def test_enviar_email_basico():
    send_mail(
        'Asunto de prueba',
        'Contenido del mensaje',
        settings.EMAIL_HOST_USER,  
        ['lucio.moro.carnero@gmail.com'],
        fail_silently=False,
    )

    assert len(mail.outbox) == 1 # 1 es que esta ok

    email = mail.outbox[0]
    assert email.from_email == settings.EMAIL_HOST_USER
    assert email.subject == 'Asunto de prueba'

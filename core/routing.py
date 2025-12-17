from django.urls import re_path

from . import consumers # pyright: ignore

websocket_urlpatterns = [
    re_path(r"ws/notif/creditos/$", consumers.CreditoConsumer.as_asgi()),
]

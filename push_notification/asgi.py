"""
ASGI config for push_notification project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'push_notification.settings')
from django.core.asgi import get_asgi_application

django_asgi_application = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from core.middleware import JWTAuthMiddleware

from .routing import websocket_urlpatterns


def JWTAuthMiddlewareStack(inner):
    return JWTAuthMiddleware(
        AuthMiddlewareStack(inner)
    )

application = ProtocolTypeRouter({
    'http': django_asgi_application,
    'websocket': JWTAuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    )
})

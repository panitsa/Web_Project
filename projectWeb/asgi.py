import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import projectWeb.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectWeb.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            projectWeb.routing.websocket_urlpatterns
        )
    ),
})

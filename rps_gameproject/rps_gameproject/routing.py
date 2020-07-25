from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
import rps_app.routing

application=ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            rps_app.routing.websocket_urlpatterns
        )
    )
})
from rest_framework.routers import DefaultRouter

from .views import (
    ClienteViewSet,
    VeiculoViewSet,
    VagaViewSet,
    ReservaViewSet,
)


router = DefaultRouter()

router.register(
    r"clientes",
    ClienteViewSet,
    basename="cliente"
)

router.register(
    r"veiculos",
    VeiculoViewSet,
    basename="veiculo"
)

router.register(
    r"vagas",
    VagaViewSet,
    basename="vaga"
)

router.register(
    r"reservas",
    ReservaViewSet,
    basename="reserva"
)

urlpatterns = router.urls
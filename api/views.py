from .models import Cliente, Veiculo, Vaga, Reserva
from .serializers import (
    ClienteSerializer,
    VeiculoSerializer,
    VagaSerializer,
    ReservaSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["nome", "cpf"]


class VeiculoViewSet(viewsets.ModelViewSet):
    queryset = Veiculo.objects.select_related("cliente").all()
    serializer_class = VeiculoSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["placa", "modelo"]


class VagaViewSet(viewsets.ModelViewSet):
    queryset = Vaga.objects.all()
    serializer_class = VagaSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["tipo", "status"]


class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.select_related(
        "veiculo",
        "vaga"
    ).all()
    serializer_class = ReservaSerializer
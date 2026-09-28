from .models import Cliente, Veiculo, Vaga, Reserva
from .serializers import (
    ClienteSerializer,
    VeiculoSerializer,
    VagaSerializer,
    ReservaSerializer,
)
from .filters import (
    ClienteFilter,
    VeiculoFilter,
    VagaFilter,
    ReservaFilter,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClienteFilter

class VeiculoViewSet(viewsets.ModelViewSet):
    queryset = Veiculo.objects.select_related("cliente").all()
    serializer_class = VeiculoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = VeiculoFilter

class VagaViewSet(viewsets.ModelViewSet):
    queryset = Vaga.objects.all()
    serializer_class = VagaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = VagaFilter

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.select_related("veiculo", "vaga").all()
    serializer_class = ReservaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReservaFilter
    
    def perform_destroy(self, instance):
        """
        Este método intercepta o verbo DELETE antes do registro sumir do banco.
        Quando a reserva é excluída, a vaga volta a ficar livre automaticamente.
        """
        vaga = instance.vaga
        vaga.status = "livre"
        vaga.save()

        instance.delete()
import django_filters

from .models import Cliente, Veiculo, Vaga, Reserva


class ClienteFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        field_name="nome",
        lookup_expr="icontains"
    )

    cpf = django_filters.CharFilter(
        field_name="cpf",
        lookup_expr="icontains"
    )

    class Meta:
        model = Cliente
        fields = ["nome", "cpf"]


class VeiculoFilter(django_filters.FilterSet):
    placa = django_filters.CharFilter(
        field_name="placa",
        lookup_expr="icontains"
    )

    modelo = django_filters.CharFilter(
        field_name="modelo",
        lookup_expr="icontains"
    )

    class Meta:
        model = Veiculo
        fields = ["placa", "modelo"]


class VagaFilter(django_filters.FilterSet):
    numero = django_filters.NumberFilter(
        field_name="numero"
    )

    tipo = django_filters.CharFilter(
        field_name="tipo"
    )

    status = django_filters.CharFilter(
        field_name="status"
    )

    class Meta:
        model = Vaga
        fields = ["numero", "tipo", "status"]


class ReservaFilter(django_filters.FilterSet):
    veiculo = django_filters.NumberFilter(
        field_name="veiculo"
    )

    vaga = django_filters.NumberFilter(
        field_name="vaga"
    )

    class Meta:
        model = Reserva
        fields = ["veiculo", "vaga"]
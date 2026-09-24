from rest_framework import serializers

from .models import Cliente, Veiculo, Vaga, Reserva


class ClienteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cliente
        fields = [
            "id",
            "nome",
            "cpf",
            "telefone",
        ]


class VeiculoSerializer(serializers.ModelSerializer):

    cliente = ClienteSerializer(read_only=True)

    cliente_id = serializers.PrimaryKeyRelatedField(
        source="cliente",
        queryset=Cliente.objects.all(),
        write_only=True
    )

    class Meta:
        model = Veiculo
        fields = [
            "id",
            "placa",
            "modelo",
            "cliente",
            "cliente_id",
        ]


class VagaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vaga
        fields = [
            "id",
            "numero",
            "tipo",
            "status",
        ]


class ReservaSerializer(serializers.ModelSerializer):

    veiculo = VeiculoSerializer(read_only=True)

    veiculo_id = serializers.PrimaryKeyRelatedField(
        source="veiculo",
        queryset=Veiculo.objects.all(),
        write_only=True
    )

    vaga = VagaSerializer(read_only=True)

    vaga_id = serializers.PrimaryKeyRelatedField(
        source="vaga",
        queryset=Vaga.objects.all(),
        write_only=True
    )

    class Meta:
        model = Reserva
        fields = [
            "id",
            "veiculo",
            "veiculo_id",
            "vaga",
            "vaga_id",
            "data_entrada",
            "data_saida",
        ]
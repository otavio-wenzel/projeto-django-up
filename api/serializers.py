from rest_framework import serializers
from .models import Cliente, Veiculo, Vaga, Reserva

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ["id", "nome", "cpf", "telefone"]

class VeiculoSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True)
    cliente_id = serializers.PrimaryKeyRelatedField(
        source="cliente",
        queryset=Cliente.objects.all(),
        write_only=True
    )

    class Meta:
        model = Veiculo
        fields = ["id", "placa", "modelo", "cliente", "cliente_id"]

class VagaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaga
        fields = ["id", "numero", "tipo", "status"]
        
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
            "data_saida"
        ]

    def validate(self, data):
        veiculo = data.get(
            "veiculo",
            self.instance.veiculo if self.instance else None
        )

        vaga = data.get(
            "vaga",
            self.instance.vaga if self.instance else None
        )

        data_entrada = data.get(
            "data_entrada",
            self.instance.data_entrada if self.instance else None
        )

        data_saida = data.get(
            "data_saida",
            self.instance.data_saida if self.instance else None
        )
        
        if data_entrada and data_saida and data_entrada >= data_saida:
            raise serializers.ValidationError({
                "data_saida": "A data de saída deve ser posterior à data de entrada."
            })
        
        if vaga and data_entrada and data_saida:
            reservas_vaga = Reserva.objects.filter(
                vaga=vaga,
                data_entrada__lt=data_saida,
                data_saida__gt=data_entrada
            )

            if self.instance:
                reservas_vaga = reservas_vaga.exclude(
                    id=self.instance.id
                )

            if reservas_vaga.exists():
                raise serializers.ValidationError({
                    "vaga": "Esta vaga já possui uma reserva confirmada para este período."
                })
            
        if veiculo and data_entrada and data_saida:
            reservas_veiculo = Reserva.objects.filter(
                veiculo=veiculo,
                data_entrada__lt=data_saida,
                data_saida__gt=data_entrada
            )

            if self.instance:
                reservas_veiculo = reservas_veiculo.exclude(
                    id=self.instance.id
                )

            if reservas_veiculo.exists():
                raise serializers.ValidationError({
                    "veiculo_id": "Este veículo já possui uma reserva para este período."
                })

        return data

    def create(self, validated_data):
        reserva = super().create(validated_data)
        vaga = reserva.vaga
        vaga.status = "reservada"
        vaga.save()

        return reserva

    def update(self, instance, validated_data):
        vaga_antiga = instance.vaga

        vaga_nova = validated_data.get("vaga", vaga_antiga)

        reserva = super().update(instance, validated_data)

        if vaga_nova != vaga_antiga:
            vaga_antiga.status = "livre"
            vaga_antiga.save()

            vaga_nova.status = "reservada"
            vaga_nova.save()

        return reserva
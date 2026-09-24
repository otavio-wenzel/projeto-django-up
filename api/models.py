from django.db import models


class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome


class Veiculo(models.Model):
    placa = models.CharField(max_length=8, unique=True)
    modelo = models.CharField(max_length=100)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="veiculos"
    )

    def __str__(self):
        return self.placa


class Vaga(models.Model):
    TIPO_CHOICES = [
        ("coberta", "Coberta"),
        ("descoberta", "Descoberta"),
    ]

    STATUS_CHOICES = [
        ("livre", "Livre"),
        ("ocupada", "Ocupada"),
        ("reservada", "Reservada"),
    ]

    numero = models.PositiveIntegerField(unique=True)
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="livre"
    )

    def __str__(self):
        return f"Vaga {self.numero}"


class Reserva(models.Model):
    veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.CASCADE,
        related_name="reservas"
    )
    vaga = models.ForeignKey(
        Vaga,
        on_delete=models.CASCADE,
        related_name="reservas"
    )
    data_entrada = models.DateTimeField()
    data_saida = models.DateTimeField()

    def __str__(self):
        return f"{self.veiculo.placa} - Vaga {self.vaga.numero}"
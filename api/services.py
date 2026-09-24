from .models import Marca

class MarcaService:

    @staticmethod
    def criar(nome, pais_origem):

        if len(nome) <= 5:
            raise Exception("dsadasdasd");

        return Marca.objects.create(
            nome=nome,
            pais_origem=pais_origem
        )
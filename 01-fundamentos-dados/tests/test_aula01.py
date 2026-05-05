import pytest
from src.aula01 import RegistroPaciente

def test_validacao_setor_correto():
    # Teste de sucesso
    assert RegistroPaciente(id=1, nome="Teste", setor="UTI")

def test_validacao_setor_errado():
    # Teste de falha esperada
    with pytest.raises(ValueError):
        RegistroPaciente(id=2, nome="Erro", setor="Cozinha")
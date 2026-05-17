import pytest
from src.aula00 import (
    limpar_dados_in_place,
    limpar_dados_seguro,
    MockConexaoSFTP
)

def test_tipagem_forte_type_error():
    """Garante que o Python mantém a tipagem forte levantando TypeError em operações incoerentes."""
    with pytest.raises(TypeError):
        # Operação proibida sem conversão explícita
        "10" + 20 # type: ignore


def test_efeito_colateral_mutabilidade():
    """Valida a mutabilidade in-place e comprova o efeito colateral indesejado em variáveis compartilhadas."""
    registro = {"id": 1, "nome": "Herbert"}
    limpar_dados_in_place(registro)
    
    # O objeto original foi modificado!
    assert registro["processado"] is True


def test_copia_segura_sem_efeito_colateral():
    """Garante que a cópia de dicionários previne efeitos colaterais de mutabilidade em pipelines de dados."""
    registro = {"id": 2, "nome": "Ana"}
    copia_limpa = limpar_dados_seguro(registro)
    
    # O original deve estar intacto
    assert "processado" not in registro
    
    # A cópia deve ter a nova chave processado
    assert copia_limpa["processado"] is True
    assert copia_limpa["id"] == 2


def test_gerenciador_de_contexto_customizado():
    """Valida o funcionamento e a resiliência do protocolo de Gerenciador de Contexto (__enter__ e __exit__)."""
    # Instanciando
    sftp = MockConexaoSFTP("sftp.teste.com")
    assert sftp.aberto is False
    
    # Entrando no contexto
    with sftp as conexao:
        assert sftp.aberto is True
        assert conexao is sftp
        
    # Saindo do contexto
    assert sftp.aberto is False

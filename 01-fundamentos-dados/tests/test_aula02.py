# pyrefly: ignore [missing-import]
import pytest
# pyrefly: ignore [missing-import]
from pydantic import ValidationError
from src.aula02 import (
    PacienteIngestionSchema,
    ConexaoBancoOracle,
    DataReaderFactory,
    CSVReader,
    JSONReader,
    DatabaseConnectionException
)

def test_pydantic_schema_valido():
    """Valida que o schema aceita registros clínicos formatados corretamente."""
    dados = {"id": 1, "nome": "Herbert", "idade": 30, "setor": "UTI"}
    paciente = PacienteIngestionSchema(**dados)
    assert paciente.id == 1
    assert paciente.nome == "Herbert"
    assert paciente.idade == 30
    assert paciente.setor == "UTI"


def test_pydantic_schema_rejeita_idade_invalida():
    """Valida se as restrições de idade (< 0 ou > 120) disparam ValidationError."""
    # Negativa
    with pytest.raises(ValidationError):
        PacienteIngestionSchema(id=2, nome="Ana", idade=-1, setor="UTI")

    # Acima de 120
    with pytest.raises(ValidationError):
        PacienteIngestionSchema(id=3, nome="Carlos", idade=121, setor="UTI")


def test_pydantic_schema_rejeita_setor_invalido():
    """Garante que setores fora da lista regulamentada (UTI, Emergência, Radiologia) são rejeitados."""
    with pytest.raises(ValidationError):
        # Cozinha é um setor inválido no hospital para internação clínica
        PacienteIngestionSchema(id=4, nome="Lucas", idade=40, setor="Cozinha")


def test_singleton_conexao_banco():
    """Garante que a classe de conexão com o banco Oracle implementa estritamente o padrão Singleton."""
    conexao_1 = ConexaoBancoOracle()
    conexao_2 = ConexaoBancoOracle()
    
    # Ambas devem apontar para a mesma e exata instância física de memória
    assert conexao_1 is conexao_2
    
    # Mudanças de estado de uma afetam a outra
    conexao_1.conectar()
    assert conexao_2._conectado is True
    
    conexao_2.desconectar()
    assert conexao_1._conectado is False


def test_factory_leitores():
    """Garante que a Factory instancia leitores de arquivo apropriados dinamicamente."""
    leitor_csv = DataReaderFactory.obter_leitor("csv")
    assert isinstance(leitor_csv, CSVReader)
    
    leitor_json = DataReaderFactory.obter_leitor("json")
    assert isinstance(leitor_json, JSONReader)
    
    # Deve disparar ValueError para formatos não suportados pela fábrica
    with pytest.raises(ValueError):
        DataReaderFactory.obter_leitor("parquet")

import pytest
import sys
from dataclasses import FrozenInstanceError
from src.aula01 import (
    RegistroClinico,
    MetricasIngestao,
    simular_leitura_streaming_csv,
    processar_pipeline_dados
)

def test_dataclass_registro_clinico_imutabilidade():
    """Garante que o schema de dados clínicos é imutável (frozen=True)."""
    registro = RegistroClinico(
        paciente_id=1,
        nome="Herbert",
        codigo_setor="UTI",
        setor_nome="Unidade de Terapia Intensiva",
        temperatura=36.7
    )
    
    # Tentar reescrever um valor deve levantar FrozenInstanceError
    with pytest.raises(FrozenInstanceError):
        registro.temperatura = 38.5 # type: ignore


def test_generator_streaming_csv_eficiencia():
    """Garante que a simulação de streaming de CSV retorna um generator de baixo consumo de RAM."""
    stream = simular_leitura_streaming_csv(5)
    
    # Deve ser um generator (iterável), não uma lista carregada em memória
    assert hasattr(stream, '__iter__')
    assert hasattr(stream, '__next__')
    
    registros = list(stream)
    assert len(registros) == 5
    assert registros[0]["paciente_id"] == 1


def test_namedtuple_metricas_ingestao():
    """Valida as propriedades do NamedTuple usado para telemetria."""
    metricas = MetricasIngestao(
        total_lidos=10,
        total_validos=8,
        total_duplicados=2,
        tempo_total_segundos=0.15
    )
    
    assert metricas.total_lidos == 10
    assert metricas.total_validos == 8
    assert metricas.total_duplicados == 2
    assert metricas.tempo_total_segundos == 0.15
    
    # Deve ser imutável
    with pytest.raises(AttributeError):
        metricas.total_lidos = 11 # type: ignore


def test_pipeline_deduplicacao_e_metricas():
    """Garante que a lógica de deduplicação O(1) de registros repetidos funciona perfeitamente."""
    # O mock do generator duplica IDs múltiplos de 5.
    # Ex: para 10 registros, IDs gerados: 1, 2, 3, 4, 4 (duplicado), 6, 7, 8, 9, 9 (duplicado).
    # Total de duplicados esperado: 2
    metricas = processar_pipeline_dados(10)
    
    assert metricas.total_lidos == 10
    assert metricas.total_validos == 8
    assert metricas.total_duplicados == 2
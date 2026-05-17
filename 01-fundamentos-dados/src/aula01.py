"""
================================================================================
🏗️ PÓS-GRADUAÇÃO EM ENGENHARIA DE DADOS & IA
🏫 MÓDULO: FUNDAMENTOS DE DADOS COM PYTHON
🎓 AULA 01: Core Python, Gestão de Memória e Estruturas de Dados Avançadas
================================================================================

Esta aula foi estruturada para ir muito além do "saber programar". O objetivo aqui é
entender como o Python lida com alocação de memória, estruturas de dados de alta
performance e tipagem forte em cenários reais de processamento de dados (ETL/ELT).

TÓPICOS ABORDADOS NESTA AULA:
1. 💡 Gestão de Memória: Generators (yield) vs Listas (RAM em O(1) vs O(N)).
2. 🏷️ Tipagem Forte (Type Hinting) aplicada a pipelines de dados.
3. 📦 Data Classes (frozen=True) para esquemas imutáveis de dados.
4. 🔢 NamedTuples para metadados e estatísticas de execução de alta performance.
5. ⚡ Otimização em O(1): Sets e Dicts para deduplicação instantânea.
6. ⏱️ Decorador Customizado (@logger_custom) para auditoria e telemetria de pipelines.
"""

import time
import sys
import logging
from dataclasses import dataclass
from typing import Generator, Dict, Any, Set, NamedTuple, List
from functools import wraps

# Configuração de Log Profissional e Estruturado
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | [AULA-01] | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


# ================================================================================
# ⏱️ 6. DECORADOR CUSTOMIZADO DE TELEMETRIA
# ================================================================================
def logger_custom(funcao):
    """
    Decorator profissional para auditoria de tempo e monitoramento de pipelines.
    Mede a latência de execução de qualquer função de ETL e loga o resultado.
    """
    @wraps(funcao)
    def wrapper(*args, **kwargs):
        logger.info(f"Iniciando execução da etapa: '{funcao.__name__}'...")
        inicio = time.perf_counter()
        
        resultado = funcao(*args, **kwargs)
        
        fim = time.perf_counter()
        duracao = fim - inicio
        logger.info(f"Etapa '{funcao.__name__}' concluída com sucesso em {duracao:.6f} segundos.")
        return resultado
    return wrapper


# ================================================================================
# 🔢 4. NAMEDTUPLES PARA ESTATÍSTICAS DE PIPELINE
# ================================================================================
class MetricasIngestao(NamedTuple):
    """
    NamedTuples são ideais para armazenar estatísticas e metadados de pipelines.
    - Ocupam muito menos memória do que dicionários (sem overhead de tabela hash).
    - São imutáveis por definição, garantindo a integridade dos metadados.
    - Permitem acesso por nome de campo (ex: metricas.total_linhas) e índice.
    """
    total_lidos: int
    total_validos: int
    total_duplicados: int
    tempo_total_segundos: float


# ================================================================================
# 📦 3. DATACLASSES PARA ESQUEMAS IMUTÁVEIS (Data Quality)
# ================================================================================
@dataclass(frozen=True)
class RegistroClinico:
    """
    DataClass imutável (frozen=True) representando um registro de entrada (Schema).
    - Imutabilidade previne alterações acidentais de dados durante o processamento.
    - Suporta Type Hinting de forma nativa.
    - Gera automaticamente construtores, representações e comparadores.
    """
    paciente_id: int
    nome: str
    codigo_setor: str
    setor_nome: str
    temperatura: float


# ================================================================================
# 💡 1. GESTÃO DE MEMÓRIA: GENERATORS (YIELD) vs LISTAS
# ================================================================================
def simular_leitura_streaming_csv(total_linhas: int) -> Generator[Dict[str, Any], None, None]:
    """
    Simula a leitura de um arquivo CSV gigantesco linha por linha.
    
    CONCEITO DE MEMÓRIA (Pós-Graduação):
    - Se usássemos uma LISTA comum (`return [dados]`), carregaríamos TODOS os milhões de 
      registros para a memória RAM de uma vez, podendo estourar o servidor (O(N) de RAM).
    - Usando GENERATORS com `yield`, o Python entrega um registro por vez sob demanda.
      A RAM permanece constante em O(1), independente se processamos 10 registros ou 10 bilhões!
    """
    # Lista de setores do Hospital da Restauração para a simulação
    setores_mock = ["UTI", "EME", "RAD", "PED"]
    
    for i in range(1, total_linhas + 1):
        # Gerando dados simulados (incluindo alguns ID duplicados propositalmente para testar deduplicação)
        paciente_id = i if i % 5 != 0 else i - 1
        
        registro = {
            "paciente_id": paciente_id,
            "nome": f"Paciente_{paciente_id}",
            "codigo_setor": setores_mock[i % len(setores_mock)],
            "temperatura": round(36.5 + (i % 3) * 0.7, 2)
        }
        yield registro


# ================================================================================
# ⚡ 5. OTIMIZAÇÃO O(1): SETS & DICTS PARA DEDUPLICAÇÃO E LOOKUP
# ================================================================================
# Dicts em Python utilizam tabelas Hash sob o capô, permitindo buscas em tempo constante O(1).
DE_PARA_SETORES: Dict[str, str] = {
    "UTI": "Unidade de Terapia Intensiva",
    "EME": "Pronto-Socorro / Emergência",
    "RAD": "Radiologia e Imagem",
    "PED": "Ala Pediátrica"
}


@logger_custom
def processar_pipeline_dados(total_registros: int) -> MetricasIngestao:
    """
    Pipeline principal de Ingestão de Dados utilizando as melhores práticas
    de performance e otimização de memória do Python.
    """
    inicio_tempo = time.perf_counter()
    
    # ⚡ O(1) de Busca: Usar um 'Set' para deduplicação instantânea.
    # Evita varrer uma lista em O(N), o que tornaria o pipeline lento exponencialmente à medida que cresce.
    ids_processados: Set[int] = set()
    
    registros_validos: List[RegistroClinico] = []
    total_lidos = 0
    total_duplicados = 0
    
    # 💡 Consumo O(1) de RAM: streaming de registros com generator
    stream_dados = simular_leitura_streaming_csv(total_registros)
    
    # Medindo tamanho inicial em memória do generator vs lista equivalente
    logger.info(f"Espaço em memória do Generator Stream: {sys.getsizeof(stream_dados)} bytes.")
    
    for linha_crua in stream_dados:
        total_lidos += 1
        p_id = linha_crua["paciente_id"]
        
        # ⚡ Deduplicação ultra veloz em O(1)
        if p_id in ids_processados:
            total_duplicados += 1
            continue
            
        ids_processados.add(p_id)
        
        # ⚡ Tradução ultra veloz em O(1) usando o dicionário (De-Para)
        cod_setor = linha_crua["codigo_setor"]
        setor_completo = DE_PARA_SETORES.get(cod_setor, "Setor Desconhecido")
        
        # Criando a representação imutável com a DataClass
        registro_limpo = RegistroClinico(
            paciente_id=p_id,
            nome=linha_crua["nome"],
            codigo_setor=cod_setor,
            setor_nome=setor_completo,
            temperatura=linha_crua["temperatura"]
        )
        registros_validos.append(registro_limpo)

    fim_tempo = time.perf_counter()
    tempo_execucao = fim_tempo - inicio_tempo
    
    # Gerando as métricas imutáveis usando a NamedTuple
    metricas = MetricasIngestao(
        total_lidos=total_lidos,
        total_validos=len(registros_validos),
        total_duplicados=total_duplicados,
        tempo_total_segundos=tempo_execucao
    )
    
    logger.info(f"Estatísticas Finais: Lidos={metricas.total_lidos} | Válidos={metricas.total_validos} | Duplicados={metricas.total_duplicados}")
    return metricas


if __name__ == "__main__":
    logger.info("=== [INICIANDO DEMONSTRAÇÃO PRÁTICA DA AULA 01] ===")
    
    # Executa o pipeline simulando 10.000 registros clínicos
    # Mesmo com 10.000 registros, o consumo de RAM é baixíssimo devido ao Generator
    metricas_finais = processar_pipeline_dados(10000)
    
    print("\n" + "="*50)
    print("=== RELATÓRIO DO PIPELINE (NAMEDTUPLE - IMUTÁVEL) ===")
    print(f"Total de registros consumidos do CSV: {metricas_finais.total_lidos}")
    print(f"Total de registros válidos ingeridos: {metricas_finais.total_validos}")
    print(f"Registros duplicados rejeitados (O(1) Set): {metricas_finais.total_duplicados}")
    print(f"Tempo total de Ingestão: {metricas_finais.tempo_total_segundos:.6f} segundos")
    print("="*50 + "\n")
    
    logger.info("=== [DEMONSTRAÇÃO PRÁTICA DA AULA 01 CONCLUÍDA] ===")
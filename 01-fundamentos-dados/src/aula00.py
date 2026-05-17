"""
================================================================================
🏗️ PÓS-GRADUAÇÃO EM ENGENHARIA DE DADOS & IA
🏫 MÓDULO: FUNDAMENTOS DE DADOS COM PYTHON
🎓 AULA 00: Introdução, Filosofia do Python e Fundamentos da Linguagem
================================================================================

Esta aula estabelece a base conceitual absoluta sobre como o interpretador Python 
funciona sob o capô. Para engenheiros de dados, entender referências de objetos, 
mutabilidade e escopos é fundamental para evitar bugs invisíveis e vazamentos de 
recursos em pipelines de produção.

TÓPICOS ABORDADOS NESTA AULA:
1. 🏷️ Tipagem Dinâmica e Forte (Por que "2" + 2 gera erro no Python).
2. 🔗 Referências de Objetos e Mutabilidade vs Imutabilidade (Variáveis como etiquetas).
3. ♻️ O Efeito Colateral em Dados (Cuidado ao modificar listas/dicionários compartilhados).
4. ⚡ Iterações Eficientes: List, Dict e Set Comprehensions (Performance do compilador).
5. 🎛️ Assinaturas Flexíveis: *args e **kwargs em funções de ETL dinâmicas.
6. 🔒 Gerenciadores de Contexto (Context Managers - o comando 'with') e segurança de IO.
7. 🛠️ Funções Embutidas (Built-ins) úteis para dados: zip, enumerate, filter.
"""

import sys
import logging
from typing import List, Dict, Tuple, Any

# Configuração de Log Profissional e Estruturado
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | [AULA-00] | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


# ================================================================================
# 🏷️ 1. TIPAGEM DINÂMICA E FORTE
# ================================================================================
def demonstrar_tipagem() -> None:
    """
    Explica a natureza da tipagem do Python.
    - Dinâmica: O tipo do objeto é determinado em tempo de execução (runtime).
    - Forte: O Python não realiza conversões implícitas absurdas (ex: somar texto e número).
    """
    logger.info("--- 1. Tipagem Dinâmica e Forte ---")
    x = 42
    logger.info(f"x é do tipo: {type(x)} e vale {x}")
    x = "Pós-Graduação" # O tipo da variável muda dinamicamente porque ela é apenas uma referência
    logger.info(f"x agora é do tipo: {type(x)} e vale '{x}'")
    
    # Demonstração de Tipagem Forte
    try:
        # Tentar somar um inteiro com uma string lança um TypeError imediatamente
        resultado = 10 + "20"
    except TypeError as te:
        logger.info(
            f"[SUCESSO DE SEGURANÇA] Python impediu somar int com str: {te}. "
            "Isso evita que dados sujos se misturem silenciosamente em pipelines."
        )


# ================================================================================
# 🔗 2. REFERÊNCIAS A OBJETOS, MUTABILIDADE & IMUTABILIDADE
# ================================================================================
def demonstrar_mutabilidade() -> None:
    """
    Em Python, variáveis NÃO SÃO caixas que guardam valores.
    Variáveis são etiquetas (pointers) coladas em objetos na memória Heap.
    
    - Imutáveis: int, float, str, tuple, frozenset. (Não podem ser alterados depois de criados).
    - Mutáveis: list, dict, set. (Podem ser alterados in-place na memória).
    """
    logger.info("--- 2. Referências e Mutabilidade ---")
    
    # Tipos Imutáveis
    a = "Dados"
    b = a
    logger.info(f"a e b apontam para o mesmo objeto? {a is b} (IDs de memória id(a)={id(a)} e id(b)={id(b)})")
    a = a + " Engineering" # Cria um NOVO objeto str e atualiza 'a' para apontar para ele.
    logger.info(f"Após modificação, b permanece '{b}' e a virou '{a}' (id(a) mudou para {id(a)})")
    
    # Tipos Mutáveis (O Perigo!)
    lista_original = [1, 2, 3]
    lista_copia = lista_original # Copia apenas a referência!
    
    lista_original.append(4)
    logger.info(f"lista_original modificada: {lista_original}")
    logger.info(
        f"lista_copia também foi alterada? {lista_copia}! "
        "Isso ocorre porque ambas compartilham o mesmo ID de memória in-place."
    )


# ================================================================================
# ⚡ 3. EVITANDO EFEITOS COLATERAIS EM PIPELINES
# ================================================================================
def limpar_dados_in_place(registro: Dict[str, Any]) -> None:
    """Modifica o dicionário original in-place. Cuidado: isso afeta outras variáveis!"""
    registro["processado"] = True


def limpar_dados_seguro(registro: Dict[str, Any]) -> Dict[str, Any]:
    """Retorna um novo dicionário na memória sem afetar o objeto original (Seguro)."""
    novo_registro = registro.copy() # Cópia rasa (shallow copy)
    novo_registro["processado"] = True
    return novo_registro


def demonstrar_efeitos_colaterais() -> None:
    logger.info("--- 3. Efeitos Colaterais em Ingestão de Dados ---")
    dado_bruto = {"id": 99, "nome": "Hospital Restauração"}
    
    # ⚠️ Forma insegura (altera a fonte original de forma indesejada)
    limpar_dados_in_place(dado_bruto)
    logger.info(f"Após in-place, o dado bruto original mudou para: {dado_bruto}")
    
    # 🟢 Forma segura (preserva o histórico bruto original)
    dado_bruto_novo = {"id": 100, "nome": "Hospital Oswaldo Cruz"}
    dado_limpo = limpar_dados_seguro(dado_bruto_novo)
    logger.info(f"Dado bruto original preservado: {dado_bruto_novo}")
    logger.info(f"Dado processado retornado em nova instância: {dado_limpo}")


# ================================================================================
# ⚡ 4. ITERAÇÕES E COMPREHENSIONS EFICIENTES (Performance)
# ================================================================================
def demonstrar_comprehensions() -> None:
    """
    List/Dict/Set Comprehensions são mais eficientes do que loops 'for' padrão.
    O interpretador do Python otimiza essas expressões em nível de bytecode, 
    executando iterações em velocidade próxima a linguagens compiladas (C).
    """
    logger.info("--- 4. Comprehensions vs Loops Tradicionais ---")
    
    # Loop Tradicional
    quadrados_loop = []
    for i in range(5):
        quadrados_loop.append(i ** 2)
        
    # List Comprehension (Mais rápido e limpo)
    quadrados_comp = [i ** 2 for i in range(5)]
    logger.info(f"List Comprehension: {quadrados_comp}")
    
    # Set Comprehension (Garante unicidade)
    set_numeros = {i % 2 for i in [1, 2, 2, 3, 4, 4, 5]}
    logger.info(f"Set Comprehension (Deduplicado): {set_numeros}")
    
    # Dict Comprehension (Mapeamentos instantâneos)
    de_para_ids = {f"ID_{i}": i * 10 for i in range(1, 4)}
    logger.info(f"Dict Comprehension: {de_para_ids}")


# ================================================================================
# 🎛️ 5. ASSINATURAS FLEXÍVEIS: *args E **kwargs
# ================================================================================
def configurar_pipeline_etl(nome_pipeline: str, *etapas: str, **opcoes: Any) -> None:
    """
    Uso de *args e **kwargs para criar funções genéricas de orquestração.
    - *etapas (*args): Captura múltiplos argumentos posicionais como uma Tupla.
    - **opcoes (**kwargs): Captura múltiplos argumentos nomeados como um Dicionário.
    """
    logger.info(f"--- 5. Configuração Dinâmica de Pipeline: '{nome_pipeline}' ---")
    logger.info(f"Etapas sequenciais informadas (*args): {etapas} (Tipo: {type(etapas)})")
    logger.info(f"Opções de infraestrutura informadas (**kwargs): {opcoes} (Tipo: {type(opcoes)})")
    
    if opcoes.get("usar_gpu", False):
        logger.info("-> Pipeline configurado para aceleração em GPU corporativa.")
    else:
        logger.info("-> Pipeline configurado para execução padrão em CPU.")


# ================================================================================
# 🔒 6. GERENCIADORES DE CONTEXTO (CONTEXT MANAGERS - the 'with' statement)
# ================================================================================
class MockConexaoSFTP:
    """
    Um gerenciador de contexto customizado demonstrando o protocolo `__enter__` e `__exit__`.
    Extremamente útil para garantir conexões SFTP ou leitura de arquivos sem vazamentos.
    """
    def __init__(self, servidor: str):
        self.servidor = servidor
        self.aberto = False

    def __enter__(self):
        logger.info(f"Conectando ao servidor SFTP em '{self.servidor}'...")
        self.aberto = True
        return self # Este objeto é injetado na variável após a palavra 'as'

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info("Encerrando sessão SFTP automaticamente e liberando sockets de rede.")
        self.aberto = False
        # Retornar True suprime eventuais exceções ocorridas no bloco. Retornar None/False propaga o erro.
        return False


def demonstrar_context_managers() -> None:
    logger.info("--- 6. Gerenciadores de Contexto (Resiliência de IO) ---")
    
    # Utilizando o Context Manager customizado
    with MockConexaoSFTP("sftp.hospital-restauracao.com") as conexao:
        logger.info(f"Sessão SFTP ativa no bloco? {conexao.aberto}")
        # Simulando leitura de dados
        logger.info("Fazendo download de logs de admissão médica...")
        
    # Ao sair do bloco 'with', o método __exit__ é invocado automaticamente, mesmo em caso de erro!
    logger.info(f"Sessão SFTP fora do bloco 'with' permanece ativa? {conexao.aberto}")


# ================================================================================
# 🛠️ 7. FUNÇÕES EMBUTIDAS (BUILT-INS) ESSENCIAIS
# ================================================================================
def demonstrar_builtins() -> None:
    logger.info("--- 7. Funções Embutidas Úteis para Engenharia de Dados ---")
    
    nomes = ["Herbert", "Ana", "Carlos"]
    idades = [29, 35, 42]
    
    # 1. zip(): Combina iteráveis paralelos em tuplas sem criar listas adicionais na RAM
    logger.info("Demonstração zip():")
    for nome, idade in zip(nomes, idades):
        logger.info(f"Paciente: {nome} | Idade: {idade}")
        
    # 2. enumerate(): Retorna índice e valor simultaneamente, ótimo para logs de linhas do CSV
    logger.info("Demonstração enumerate():")
    for idx, nome in enumerate(nomes, start=1):
        logger.info(f"Linha {idx}: Ingerindo paciente '{nome}'")
        
    # 3. filter(): Filtra elementos sob demanda usando avaliação preguiçosa (lazy evaluation)
    idades_filtradas = filter(lambda idade: idade >= 35, idades)
    logger.info(f"Idades filtradas (Generator de filtros): {idades_filtradas}")
    logger.info(f"Idades filtradas convertidas em lista: {list(idades_filtradas)}")


if __name__ == "__main__":
    logger.info("=== [INICIANDO DEMONSTRAÇÃO PRÁTICA DA AULA 00] ===")
    
    demonstrar_tipagem()
    print()
    demonstrar_mutabilidade()
    print()
    demonstrar_efeitos_colaterais()
    print()
    demonstrar_comprehensions()
    print()
    
    # Execução flexível com *args e **kwargs
    configurar_pipeline_etl(
        "ETL_Paciente_UTI",
        "Extração_SFTP", "Validação_Pydantic", "Carga_Oracle",
        usar_gpu=True,
        timeout_segundos=30
    )
    print()
    
    demonstrar_context_managers()
    print()
    demonstrar_builtins()
    
    logger.info("=== [DEMONSTRAÇÃO PRÁTICA DA AULA 00 CONCLUÍDA] ===")

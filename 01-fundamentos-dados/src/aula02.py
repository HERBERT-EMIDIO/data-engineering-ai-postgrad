"""
================================================================================
🏗️ PÓS-GRADUAÇÃO EM ENGENHARIA DE DADOS & IA
🏫 MÓDULO: FUNDAMENTOS DE DADOS COM PYTHON
🎓 AULA 02: Padrões de Projeto (Design Patterns) e Resiliência em Pipelines
================================================================================

Esta aula aprofunda conceitos de arquitetura de software aplicados a dados.
Engenheiros de Dados constroem sistemas distribuídos que operam 24/7. Erros e falhas
são a regra, não a exceção. Aqui estudamos como projetar código resiliente, modular
e de alta manutenibilidade.

TÓPICOS ABORDADOS NESTA AULA:
1. 📐 Padrão Singleton: Gerenciamento único e centralizado de conexões de banco (ex: Oracle).
2. 🏭 Padrão Factory: Criação dinâmica de leitores de arquivos heterogêneos (CSV, JSON).
3. ⚠️ Tratamento Resiliente: Try/Except/Finally para prevenção de vazamento de recursos.
4. 🏷️ Validação de Data Quality: Validação estrita de contratos de dados com Pydantic v2.
5. 🛡️ Exceções Customizadas: Criação de erros específicos de negócio/pipeline.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pydantic import BaseModel, Field, field_validator, ValidationError

# Configuração de Log Profissional e Estruturado
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | [AULA-02] | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


# ================================================================================
# 🛡️ 5. EXCEÇÕES CUSTOMIZADAS (Domain Exceptions)
# ================================================================================
class PipelineException(Exception):
    """Classe base para todas as exceções do pipeline."""
    pass

class InvalidSchemaException(PipelineException):
    """Disparada quando o esquema do registro de entrada viola as regras de qualidade."""
    pass

class DatabaseConnectionException(PipelineException):
    """Disparada quando a conexão com o banco de dados falha ou é interrompida."""
    pass


# ================================================================================
# 🏷️ 4. VALIDAÇÃO DE DATA QUALITY COM PYDANTIC V2
# ================================================================================
class PacienteIngestionSchema(BaseModel):
    """
    Schema de Ingestão de Dados utilizando Pydantic para validação robusta.
    - Garante tipos primitivos corretos.
    - Aplica regras de limites de valor (ex: idade entre 0 e 120).
    - Permite criar validadores personalizados com @field_validator.
    """
    id: int = Field(..., gt=0, description="O ID do paciente deve ser um inteiro positivo.")
    nome: str = Field(..., min_length=2, description="O nome deve conter ao menos 2 caracteres.")
    idade: int = Field(..., ge=0, le=120, description="A idade deve estar entre 0 e 120 anos.")
    setor: str = Field(..., description="Setor de atendimento (UTI, Emergência, Radiologia).")

    @field_validator('setor')
    @classmethod
    def validar_setor_restrito(cls, v: str) -> str:
        """Validador customizado: rejeita setores fora da lista oficial do Hospital."""
        setores_validos = ['UTI', 'Emergência', 'Radiologia']
        if v not in setores_validos:
            raise ValueError(f"O setor '{v}' é inválido. Setores válidos: {setores_validos}")
        return v


# ================================================================================
# 📐 1. PADRÃO SINGLETON: GERENCIADOR DE CONEXÃO COM BANCO DE DADOS
# ================================================================================
class ConexaoBancoOracle:
    """
    Implementação do Padrão Singleton.
    Garante que exista apenas UMA instância de conexão de banco ativa no pipeline.
    
    POR QUE USAR EM ENGENHARIA DE DADOS?
    - Criar conexões de rede com bancos relacionais (como Oracle ou PostgreSQL) é caro.
    - Múltiplas conexões concorrentes desnecessárias esgotam o pool do banco de dados (Crash!).
    - O Singleton centraliza o estado e reutiliza a conexão de forma segura.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ConexaoBancoOracle, cls).__new__(cls)
            # Inicializando a conexão simulada
            cls._instance._conectado = False
            cls._instance._host = "oracle-prod-hospital.local"
        return cls._instance

    def conectar(self) -> None:
        """Simula a abertura de conexão de rede."""
        if not self._conectado:
            logger.info(f"Estabelecendo conexão física com o Oracle em '{self._host}' (Abertura de Socket)...")
            self._conectado = True
        else:
            logger.debug("Reutilizando conexão Oracle ativa (Singleton funcionando!).")

    def desconectar(self) -> None:
        """Fecha a conexão simulada, liberando os sockets e memória."""
        if self._conectado:
            logger.info("Encerrando conexão física com o banco de dados Oracle de forma limpa.")
            self._conectado = False

    def salvar_registro(self, dados: Dict[str, Any]) -> None:
        """Insere o dado validado no banco de dados corporativo."""
        if not self._conectado:
            raise DatabaseConnectionException("Erro de Transação: O banco não está conectado!")
        logger.info(f"-> [DATABASE LOAD] Registro {dados['id']} salvo com sucesso no Oracle.")


# ================================================================================
# 🏭 2. PADRÃO FACTORY: LEITORES DINÂMICOS DE ARQUIVOS
# ================================================================================
class BaseReader(ABC):
    """Interface abstrata (Base) para todos os leitores de dados."""
    @abstractmethod
    def read(self, source_path: str) -> List[Dict[str, Any]]:
        pass


class CSVReader(BaseReader):
    """Implementação específica de leitor para arquivos CSV."""
    def read(self, source_path: str) -> List[Dict[str, Any]]:
        logger.info(f"Lendo e parseando arquivo CSV de: {source_path}")
        # Dados simulados mockados
        return [
            {"id": 101, "nome": "Herbert Emidio", "idade": 29, "setor": "UTI"},
            {"id": 102, "nome": "Ana Costa", "idade": -5, "setor": "Emergência"},  # Idade inválida (<0)
            {"id": 103, "nome": "Carlos Silva", "idade": 45, "setor": "Cozinha"},  # Setor inválido
        ]


class JSONReader(BaseReader):
    """Implementação específica de leitor para arquivos JSON."""
    def read(self, source_path: str) -> List[Dict[str, Any]]:
        logger.info(f"Lendo e parseando arquivo JSON de: {source_path}")
        return [
            {"id": 201, "nome": "Maria Souza", "idade": 34, "setor": "Radiologia"},
            {"id": 202, "nome": "Lucas Santos", "idade": 130, "setor": "UTI"},  # Idade inválida (>120)
        ]


class DataReaderFactory:
    """
    Classe Factory que instancia leitores dinamicamente.
    Permite adicionar suporte a novos formatos (ex: Parquet, XML) sem alterar
    o código do pipeline principal (Princípio Open-Closed do SOLID).
    """
    @staticmethod
    def obter_leitor(formato: str) -> BaseReader:
        formatos = {
            "csv": CSVReader,
            "json": JSONReader
        }
        formato_limpo = formato.lower().strip()
        if formato_limpo not in formatos:
            raise ValueError(f"Formato de arquivo '{formato}' não suportado pela Factory.")
        
        return formatos[formato_limpo]()


# ================================================================================
# ⚠️ 3. PIPELINE INTEGRADO E RESILIENTE (Try/Except/Finally)
# ================================================================================
def executar_pipeline_etl(origem: str, formato: str) -> None:
    """
    Pipeline de ETL resiliente que demonstra a aplicação real dos conceitos da Aula 02.
    """
    logger.info(f"=== Iniciando Pipeline de ETL para a fonte: {origem} ===")
    
    # 📐 Obter o leitor apropriado usando o padrão Factory
    leitor = DataReaderFactory.obter_leitor(formato)
    dados_brutos = leitor.read(origem)
    
    # 📐 Conectar ao Banco de Dados usando o padrão Singleton
    db = ConexaoBancoOracle()
    
    try:
        db.conectar()
        
        for linha in dados_brutos:
            try:
                # 🏷️ Validação Estrita de Qualidade usando Pydantic
                # Lança ValidationError se violar qualquer regra do schema
                paciente_validado = PacienteIngestionSchema(**linha)
                
                # Carga no banco caso o schema esteja correto
                db.salvar_registro(paciente_validado.model_dump())
                
            except ValidationError as ve:
                # Tratamento focado em Data Quality (Resiliência)
                # O pipeline não quebra ao encontrar um registro inválido.
                # Ele loga o erro, descarta o registro "sujo" (Dead Letter Queue) e prossegue.
                logger.error(
                    f"[DATA QUALITY REJECT] Registro ID {linha.get('id')} violou regras do schema! "
                    f"Detalhes do erro: {ve.errors()[0]['msg']}"
                )
            except Exception as e:
                logger.error(f"Erro inesperado no processamento do registro {linha}: {e}")
                
    except DatabaseConnectionException as dbe:
        logger.error(f"[FATAL] Falha crítica de infraestrutura: {dbe}")
        
    finally:
        # ⚠️ GARANTIA DE RESILIÊNCIA: Try/Except/Finally
        # Independentemente se o pipeline falhar com erro de banco, erro de código ou rodar limpo,
        # o bloco 'finally' GARANTE o encerramento da conexão de rede para evitar vazamento de sockets.
        db.desconectar()
        logger.info("=== Pipeline de ETL finalizado e recursos liberados ===")


if __name__ == "__main__":
    logger.info("=== [INICIANDO DEMONSTRAÇÃO PRÁTICA DA AULA 02] ===")
    
    # Executando ETL para fonte CSV (contém dados intencionalmente incorretos)
    executar_pipeline_etl("caminho/do/arquivo_pacientes.csv", "csv")
    
    print("\n" + "-"*80 + "\n")
    
    # Executando ETL para fonte JSON
    executar_pipeline_etl("caminho/do/arquivo_pacientes.json", "json")
    
    logger.info("=== [DEMONSTRAÇÃO PRÁTICA DA AULA 02 CONCLUÍDA] ===")

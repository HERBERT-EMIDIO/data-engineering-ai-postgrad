
# 🏗 Fundamentos de Engenharia de Dados com Python

Este módulo estabelece a base técnica para a construção de sistemas de dados escaláveis. O foco aqui não é apenas "saber programar", mas entender como o Python processa dados sob o capô.

## 🐍 Python para Data Engineering: Core Concepts

### 1. Gestão de Memória e Tipagem
Diferente do desenvolvimento web, em dados, a memória é o recurso mais caro.
*   **Generators vs Lists:** Uso de `yield` para processamento de arquivos gigantes sem estourar a RAM.
*   **Type Hinting:** Uso da biblioteca `typing` para garantir a integridade dos contratos de dados em pipelines.

### 2. Estruturas de Dados Avançadas
*   **Dicts & Sets:** Otimização de buscas (O(1)) para processos de *lookup* e deduplicação.
*   **Data Classes:** Implementação de schemas de dados limpos e imutáveis.
*   **NamedTuples:** Performance superior para registros de bases de dados.

### 3. Tratamento de Erros e Resiliência (Data Quality)
Em produção, pipelines falham. A estratégia aqui foca em:
*   **Try/Except/Finally:** Garantir o fechamento de conexões com bancos de dados.
*   **Logging:** Implementação de logs estruturados para monitoramento de volume e latência.
*   **Custom Exceptions:** Criação de exceções específicas para falhas de schema ou de conexão com APIs.

## 🛠 Stack de Ferramentas do Módulo
| Ferramenta | Aplicação |
| :--- | :--- |
| **Python 3.11+** | Engine principal de processamento |
| **Pandas/Polars** | Manipulação e análise de DataFrames |
| **Pydantic** | Validação de schemas de dados |
| **Pytest** | Testes unitários para transformações |

## 📐 Padrões de Projeto (Design Patterns)
*   **Singleton:** Para gerenciar conexões únicas com bancos de dados (como o Oracle do Hospital).
*   **Factory:** Para criar leitores de diferentes formatos (CSV, Parquet, JSON) dinamicamente.

## 🚀 Laboratórios Práticos
1.  **Extract_In_Memory:** Script para ler arquivos flat e converter para formatos colunares.
2.  **Validator_Schema:** Uso de Pydantic para validar entradas de dados de saúde.
3.  **Logger_Custom:** Classe de log para rastrear o tempo de execução de cada etapa do ETL.

---
**Skill Focus:** Performance, Tipagem Forte, Manutenibilidade.
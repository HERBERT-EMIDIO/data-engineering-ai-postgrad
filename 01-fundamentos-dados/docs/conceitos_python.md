# Fundamentos de Python para Engenharia de Dados

Neste módulo, exploramos como o Python sustenta pipelines de alta performance.

### 🎯 Pontos de Atenção Técnica
*   **Tipagem Forte e Hinting:** Utilizamos `typing` para garantir que os contratos de dados entre funções sejam respeitados, evitando erros de runtime em produção.
*   **Data Quality (Pydantic):** Implementamos validação de esquema na entrada (Ingestion) para garantir que apenas dados íntegros sigam para o processamento.
*   **Gerenciamento de Memória:** Foco no uso de Generators e iteradores para processar grandes volumes de dados sem saturar a RAM.
*   **Logging Estruturado:** Substituímos o `print()` por logs reais, permitindo rastrear sucessos e falhas em sistemas críticos como o do Hospital da Restauração.
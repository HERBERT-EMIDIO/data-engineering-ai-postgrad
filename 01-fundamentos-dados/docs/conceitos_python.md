# 📘 Fundamentos Teóricos e Práticos de Python para Engenharia de Dados

Este documento serve como guia acadêmico e de referência técnica para os conceitos explorados nos laboratórios práticos do **Módulo 01: Fundamentos de Dados com Python**. Aqui detalhamos a teoria por trás das escolhas de arquitetura e implementação de pipelines escaláveis.

---

## ⚡ 0. Introdução & Filosofia do Python para Engenharia de Dados

Antes de dominar padrões de design complexos, o Engenheiro de Dados precisa compreender com precisão a semântica da linguagem Python:

### 1. Tipagem Dinâmica e Forte
* **Dinâmica:** Variáveis não possuem tipo fixo; elas são apenas etiquetas que apontam para objetos na memória Heap. O tipo do objeto é resolvido em runtime.
* **Forte:** O interpretador Python impede operações lógicas incoerentes (ex: somar texto e número) sem conversão explícita. Isso serve como barreira de segurança (*Type Safety*) em pipelines para evitar a poluição de downstreams.

### 2. Referências a Objetos e Mutabilidade
Em Python, as variáveis funcionam como ponteiros (*pointers*) que rotulam objetos:
* **Imutáveis (str, int, float, tuple):** Quando modificados, o Python cria um novo objeto em outro endereço de memória. São seguros e imutáveis por definição.
* **Mutáveis (list, dict, set):** Podem ter seus elementos modificados in-place na memória compartilhada. **Cuidado:** Passar um dicionário bruto de dados clínicos para uma função e alterá-lo in-place alterará a variável original fora da função (efeito colateral), destruindo o histórico da extração. Prefira `.copy()` ou cópias profundas (*deep copy*) para preservar registros brutos.

### 3. Comprehensions e Performance
* List, Dict e Set comprehensions não são apenas açúcar sintático (*syntactic sugar*). 
* O interpretador Python compila essas expressões em nível de bytecode de forma altamente otimizada, rodando iterações muito mais rápido do que loops `for` tradicionais em nível de máquina.

### 4. Gerenciadores de Contexto (Context Managers)
* Representados pelo bloco `with` usando os métodos especiais `__enter__` e `__exit__`.
* Garantem a alocação e a liberação automática de recursos (sockets SFTP, file descriptors, conexões de APIs), mesmo diante de falhas de runtime. Isso evita que sistemas fiquem inoperantes por vazamentos de conexões.

---

## ⚡ 1. Gestão de Memória: Generators vs Listas

Em Engenharia de Dados, a memória RAM é o recurso de infraestrutura mais crítico e caro. Carregar arquivos volumosos (de gigabytes a terabytes) inteiros na memória de uma vez inviabiliza pipelines de larga escala.

### 🔴 Listas: A Armadilha de Processamento (RAM $O(N)$)
Quando uma função lê dados e retorna uma lista comum (`List`):
1. **Alocação Massiva:** O Python aloca memória no *Heap* para conter todos os itens simultaneamente.
2. **Crash do Sistema (OOM):** Se o arquivo for maior que a RAM disponível, o sistema operacional mata o processo com um erro `Out Of Memory` (OOM).
3. **Overhead de Pointer:** Listas em Python contêm ponteiros para objetos individuais, o que adiciona um overhead considerável de metadados por item na memória.

### 🟢 Generators: Ingestão em Streaming (RAM $O(1)$)
Utilizando o recurso `yield` do Python, criamos um **Generator**:
1. **Avaliação Preguiçosa (*Lazy Evaluation*):** O Python suspende o estado da função a cada `yield` e só processa o próximo elemento sob demanda de um loop.
2. **RAM Constante:** A complexidade espacial é de **$O(1)$**. O pipeline consome o mesmo volume de RAM, esteja processando $10$ registros ou $10.000.000.000$!
3. **Desempenho de Cache:** Favorece o cache de CPU, pois os dados são limpos e reciclados da memória logo após o consumo no loop.

---

## ⚡ 2. Estruturas de Dados Avançadas & Complexidade Algorítmica

### 🏎️ Complexidade de Busca: Sets/Dicts $O(1)$ vs Listas $O(N)$
A escolha da estrutura para deduplicação ou cruzamento (*lookup*) de dados define se seu pipeline levará segundos ou horas.

* **Listas ($O(N)$):** Fazer buscas do tipo `if id in lista_ids` obriga o Python a varrer toda a lista sequencialmente do início ao fim. Se temos $100.000$ registros, o loop principal fará até $100.000 \times 100.000 = 10.000.000.000$ comparações.
* **Sets/Dicionários ($O(1)$):** Utilizam **Tabelas Hash**. O Python calcula a função Hash do valor de busca e vai diretamente ao endereço de memória exato do elemento. A busca ocorre instantaneamente, independente do tamanho do conjunto.

### 📦 Data Classes (`frozen=True`) para Esquemas Limpos
Utilizamos `@dataclass(frozen=True)` para representar os dados ingeridos:
* **Integridade dos Dados:** O parâmetro `frozen=True` impede alterações acidentais de valores ao longo do pipeline (imutabilidade).
* **Tipagem Estrita:** Permite que ferramentas de análise estática e IDEs previnam bugs antes da execução.
* **Performance:** Menor overhead de criação em comparação com objetos de classes tradicionais customizadas.

### 🔢 NamedTuples para Telemetria e Metadados
NamedTuples estendem a tupla padrão permitindo indexação por nomes de campos:
* **Eficiência Extrema:** Não criam um dicionário de instância (`__dict__`), consumindo até **$3\times$ menos memória** do que classes padrão ou dicts.
* **Clareza de Código:** Substituem tuplas confusas de índices (ex: `info[0]`) por nomes legíveis (ex: `info.tempo_total`).

---

## 📐 3. Padrões de Projeto (Design Patterns) Aplicados a Dados

### 1. Padrão Singleton
No pipeline, a classe `ConexaoBancoOracle` implementa o padrão Singleton.
* **O Problema:** Abrir conexões físicas de rede (sockets) com bancos de dados relacionais é uma operação lenta e de alto custo computacional. Criar uma nova conexão para cada lote de dados estoura o pool do servidor de banco, gerando travamentos.
* **A Solução:** O Singleton garante que apenas **uma única instância de conexão física** seja criada e reutilizada em toda a vida útil do pipeline, economizando recursos de rede de forma inteligente.

### 2. Padrão Factory
A classe `DataReaderFactory` centraliza a instanciação de leitores de arquivo.
* **Design Limpo (SOLID):** Implementa o **Princípio Aberto-Fechado (Open-Closed)**. Se precisarmos ler um arquivo no formato *Parquet* amanhã, adicionamos um `ParquetReader` à Factory sem precisar tocar ou quebrar o código principal do pipeline ETL.
* **Desacoplamento:** O pipeline principal não sabe e nem precisa saber de detalhes de parsing de arquivos brutos, ele apenas consome a interface padronizada `BaseReader`.

---

## 🛡️ 4. Tratamento Resiliente de Erros e Qualidade de Dados (Data Quality)

Pipelines de produção operam sem supervisão humana contínua. Por isso, a tolerância e o tratamento profissional de anomalias são cruciais:

1. **Validação na Entrada com Pydantic:** Os dados vindos de APIs ou arquivos brutos são validados imediatamente no momento da ingestão contra um `BaseModel` estrito. Registros que violarem tipos ou regras de negócio (ex: idade inválida) são isolados (padrão *Dead Letter Queue*) e logados em nível de erro/aviso, sem derrubar a execução do pipeline inteiro.
2. **Try/Except/Finally para Segurança de Recursos:** Recursos do sistema operacional (como conexões de banco de dados e ponteiros de arquivos) são criados dentro de estruturas `try` e fechados de forma obrigatória no bloco `finally`. Isso impede vazamento de memória ou locks persistentes em servidores caso um erro crítico interrompa o fluxo principal.
3. **Exceções de Domínio:** A criação de erros customizados (ex: `InvalidSchemaException`) ajuda equipes de monitoramento (SRE/Engenharia de Dados) a identificar rapidamente através do dashboard de logs a causa exata e o contexto de uma quebra no pipeline.
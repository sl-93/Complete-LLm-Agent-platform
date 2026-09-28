# Complete LLM Agent Platform

A production-oriented LLM application built progressively from **Retrieval-Augmented Generation (RAG)** to **advanced retrieval, tool calling, autonomous agents, memory, planning, multi-agent systems, evaluation, and production deployment**.

This repository is both a practical implementation project and a learning journey focused on understanding how modern LLM applications are designed, implemented, evaluated, and deployed.

---

## 🚀 Overview

Modern LLM applications are much more than a single prompt sent to a language model.

A reliable AI system typically needs to combine:

* Large Language Models
* Retrieval-Augmented Generation
* Vector databases
* Embeddings
* Advanced retrieval strategies
* Tool calling
* Agentic workflows
* Memory
* Planning
* Multi-agent collaboration
* Evaluation
* Observability
* API services
* Production infrastructure

This project is designed to build these capabilities **incrementally in one coherent system**.

The development path is:

```text
RAG
 │
 ├── Document Ingestion
 ├── Chunking
 ├── Embeddings
 ├── Vector Search
 │
 ▼
Advanced RAG
 │
 ├── Hybrid Search
 ├── Metadata Filtering
 ├── Query Rewriting
 ├── Multi-Query Retrieval
 └── Reranking
 │
 ▼
Tool Calling
 │
 ├── Calculator
 ├── Database
 ├── External APIs
 └── Custom Tools
 │
 ▼
Agents
 │
 ├── Tool Selection
 ├── Reasoning / ReAct
 ├── Planning
 └── Task Execution
 │
 ▼
Memory
 │
 ├── Conversation Memory
 ├── Short-Term Memory
 └── Long-Term Memory
 │
 ▼
Multi-Agent Systems
 │
 ├── Specialized Agents
 ├── Agent Coordination
 └── Agent Communication
 │
 ▼
Evaluation & Observability
 │
 ├── Retrieval Evaluation
 ├── Answer Evaluation
 ├── Tracing
 ├── Metrics
 └── Cost / Latency Monitoring
 │
 ▼
Production LLM Platform
```

---

## 🎯 Project Goals

The main goals of this project are:

1. Build a complete RAG system from the ground up.
2. Understand the internal architecture of modern LLM applications.
3. Implement production-oriented retrieval pipelines.
4. Integrate LLMs with external tools and data sources.
5. Build autonomous agents capable of selecting and using tools.
6. Implement memory and planning mechanisms.
7. Explore multi-agent architectures.
8. Build evaluation and observability into the system.
9. Gradually transform the project into a deployable LLM platform.

The emphasis is on **implementation and engineering**, not only theoretical concepts.

---

## 🧠 Current Architecture

The current version focuses on the RAG layer:

```text
                    ┌──────────────────┐
                    │    Documents     │
                    │ PDF / DOCX / TXT │
                    │      / Excel     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Document         │
                    │ Ingestion        │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Chunking         │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Embeddings       │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ ChromaDB         │
                    │ Vector Store     │
                    └────────┬─────────┘
                             │
                             │
User Query ──────────────────┤
                             ▼
                    ┌──────────────────┐
                    │ Retrieval        │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Retrieved        │
                    │ Context          │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ LLM              │
                    │ Ollama / Gemma   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Final Answer     │
                    └──────────────────┘
```

---

## 🛠️ Technology Stack

| Component           | Technology                            |
| ------------------- | ------------------------------------- |
| Language            | Python                                |
| LLM Runtime         | Ollama                                |
| LLM                 | Gemma                                 |
| Embeddings          | Sentence Transformers                 |
| Vector Database     | ChromaDB                              |
| API                 | FastAPI *(planned/integration stage)* |
| Document Processing | PyPDF / python-docx / pandas          |
| Environment         | Python virtual environment            |
| Version Control     | Git / GitHub                          |

The architecture is intentionally modular so that individual components can later be replaced without redesigning the entire application.

---

## 📂 Project Structure

The project is being organized around independent components rather than putting all logic into a single application file.

```text
Complete-LLm-Agent-platform/
│
├── data/
│   └── documents/
│
├── src/
│   ├── ingestion/
│   │   ├── loaders/
│   │   └── ...
│   │
│   ├── chunking/
│   │   └── ...
│   │
│   ├── embeddings/
│   │   └── ...
│   │
│   ├── vectorstore/
│   │   └── ...
│   │
│   ├── retrieval/
│   │   └── ...
│   │
│   ├── generation/
│   │   └── ...
│   │
│   ├── tools/
│   │   └── ...
│   │
│   ├── agents/
│   │   └── ...
│   │
│   ├── memory/
│   │   └── ...
│   │
│   ├── evaluation/
│   │   └── ...
│   │
│   └── config/
│       └── ...
│
├── chroma_db/
│
├── tests/
│
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

> The structure will evolve as new capabilities are implemented.

---

# 🔎 RAG Pipeline

The initial system implements a Retrieval-Augmented Generation pipeline.

### Indexing

```text
Documents
    ↓
Text Extraction
    ↓
Chunking
    ↓
Embedding Generation
    ↓
Vector Storage
```

### Querying

```text
User Question
    ↓
Query Embedding
    ↓
Vector Search
    ↓
Relevant Documents
    ↓
Context Construction
    ↓
LLM
    ↓
Answer
```

This separates **knowledge retrieval** from **language generation**.

Instead of expecting the LLM to know every piece of information, the system retrieves relevant external knowledge and provides it as context.

---

# 📚 Advanced RAG

The next stage extends basic vector search into a more robust retrieval pipeline.

Planned components include:

### Metadata Filtering

Retrieve documents according to metadata such as:

```text
department
document_type
year
source
page
```

### Hybrid Retrieval

Combine:

```text
Dense Retrieval
      +
Lexical Retrieval
      ↓
Hybrid Ranking
```

This allows the system to benefit from both semantic similarity and exact keyword matching.

### Query Rewriting

Transform the user's original question into a retrieval-optimized query.

```text
User Question
      ↓
Query Rewriter
      ↓
Improved Search Query
      ↓
Retriever
```

### Multi-Query Retrieval

Generate multiple search queries for ambiguous or complex questions.

```text
Original Question
       ↓
 ┌─────┼─────┐
 ↓     ↓     ↓
Q1    Q2    Q3
 │     │     │
 └─────┼─────┘
       ↓
 Combined Results
       ↓
     Reranker
```

### Reranking

Initial retrieval will return a larger candidate set, which can then be reranked using a more accurate model.

```text
Query
  ↓
Top 20 Candidates
  ↓
Reranker
  ↓
Top 3 Relevant Chunks
  ↓
LLM
```

---

# 🔧 Tool Calling

After the retrieval layer, the system will be extended with external tools.

Example:

```text
User
 ↓
LLM
 ↓
Tool Selection
 ├── Calculator
 ├── Database
 ├── Search
 ├── Python
 └── External API
 ↓
Tool Result
 ↓
LLM
 ↓
Final Answer
```

The goal is to allow the model to interact with external systems instead of relying only on generated text.

---

# 🤖 Agents

The next stage introduces agentic behavior.

Instead of:

```text
Question → LLM → Answer
```

the system will support:

```text
Question
   ↓
Agent
   ↓
Plan / Decide
   ↓
Select Tool
   ↓
Execute Tool
   ↓
Observe Result
   ↓
Decide Next Action
   ↓
Final Answer
```

The agent layer will explore concepts such as:

* ReAct
* Tool selection
* Task decomposition
* Planning
* Iterative execution
* Agent state
* Error handling
* Guardrails

---

# 🧠 Memory

The platform will gradually support different forms of memory.

### Short-Term Memory

Conversation context within a session.

```text
User
 ↓
Conversation
 ↓
Recent Messages
 ↓
LLM
```

### Long-Term Memory

Important information can be stored and retrieved across conversations.

```text
Conversation
     ↓
Memory Extraction
     ↓
Memory Store
     ↓
Future Conversation
     ↓
Memory Retrieval
     ↓
LLM
```

Memory will be treated as a separate system component rather than tightly coupling it to the agent implementation.

---

# 🤝 Multi-Agent Systems

The platform will eventually support multiple specialized agents.

For example:

```text
                    ┌───────────────┐
                    │ Orchestrator  │
                    └───────┬───────┘
                            │
          ┌─────────────────┼─────────────────┐
          ↓                 ↓                 ↓
   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
   │ Researcher  │   │  Analyst    │   │  Executor   │
   │    Agent    │   │    Agent    │   │    Agent    │
   └─────────────┘   └─────────────┘   └─────────────┘
          │                 │                 │
          └─────────────────┼─────────────────┘
                            ↓
                       Final Result
```

Possible responsibilities include:

* Research
* Retrieval
* Data analysis
* Planning
* Execution
* Verification

---

# 📊 Evaluation & Observability

A production LLM system needs more than functional code.

The project will therefore introduce evaluation and observability as first-class components.

### Retrieval Evaluation

Examples:

* Recall@K
* Precision@K
* MRR
* Context relevance

### Generation Evaluation

Examples:

* Faithfulness
* Answer relevance
* Groundedness
* Citation accuracy

### System Metrics

```text
Latency
Token Usage
Cost
Success Rate
Failure Rate
Tool Calls
Retrieval Quality
```

The long-term objective is to make system behavior measurable rather than relying only on manual inspection.

---

# 🏗️ Production Architecture

The final architecture is intended to evolve toward:

```text
                         ┌─────────────────┐
                         │     Client      │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │    FastAPI      │
                         │      API        │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ Agent Runtime   │
                         └────────┬────────┘
                                  │
                ┌─────────────────┼─────────────────┐
                │                 │                 │
                ▼                 ▼                 ▼
          ┌───────────┐    ┌───────────┐    ┌───────────┐
          │   RAG     │    │   Tools   │    │  Memory   │
          └─────┬─────┘    └─────┬─────┘    └─────┬─────┘
                │                 │                 │
                ▼                 ▼                 ▼
          ┌───────────┐    ┌───────────┐    ┌───────────┐
          │ Vector DB │    │ External  │    │ Memory DB │
          │           │    │ Systems   │    │           │
          └───────────┘    └───────────┘    └───────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │      LLM        │
                         └─────────────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ Evaluation &    │
                         │ Observability   │
                         └─────────────────┘
```

---

# 🗺️ Roadmap

The project is developed incrementally.

* [x] Project initialization
* [x] Basic document ingestion
* [x] Text chunking
* [x] Embedding generation
* [x] ChromaDB integration
* [x] Basic semantic retrieval
* [x] LLM generation with retrieved context
* [ ] Metadata-aware retrieval
* [ ] Hybrid search
* [ ] Query rewriting
* [ ] Multi-query retrieval
* [ ] Reranking
* [ ] Retrieval evaluation
* [x] Tool calling
* [x] Tool registry
* [ ] Agent runtime
* [ ] ReAct-style agents
* [ ] Planning
* [ ] Short-term memory
* [ ] Long-term memory
* [ ] Multi-agent orchestration
* [ ] Agent evaluation
* [ ] Observability
* [ ] API layer
* [ ] Dockerization
* [ ] CI/CD
* [ ] Production deployment

---

# 📖 Learning & Research

The implementation is accompanied by research papers and technical concepts from modern LLM literature.

Selected foundational papers include:

* **Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks** — Lewis et al., 2020
* **Dense Passage Retrieval for Open-Domain Question Answering** — Karpukhin et al., 2020
* **Sentence-BERT** — Reimers & Gurevych, 2019
* **ColBERT** — Khattab & Zaharia, 2020
* **Lost in the Middle** — Liu et al., 2023
* **ReAct: Synergizing Reasoning and Acting in Language Models** — Yao et al., 2022
* **Toolformer** — Schick et al., 2023
* **LoRA** — Hu et al., 2021
* **QLoRA** — Dettmers et al., 2023

The purpose is not only to use existing frameworks, but to understand the design decisions behind the systems being built.

---

# ⚙️ Getting Started

## 1. Clone the repository

```bash
git clone https://github.com/sl-93/Complete-LLm-Agent-platform.git

cd Complete-LLm-Agent-platform
```

## 2. Create a virtual environment

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Install and run Ollama

Make sure Ollama is installed and running locally.

Pull the required model:

```bash
ollama pull gemma4:e2b
```

You can verify the model with:

```bash
ollama list
```

## 5. Run the application

```bash
python main.py
```

---

# 🔐 Environment Variables

Sensitive configuration should not be committed to Git.

Create a local `.env` file when required:

```env
OLLAMA_HOST=http://localhost:11434
LLM_MODEL=gemma4:e2b
```

Use `.env.example` as a template for required configuration.

---

# 🧪 Testing

Tests will be introduced progressively as the system becomes more modular.

The planned test structure is:

```text
tests/
├── ingestion/
├── chunking/
├── embeddings/
├── retrieval/
├── generation/
├── tools/
├── agents/
└── evaluation/
```

The goal is to test individual components independently before testing complete agent workflows.

---

# 🧩 Design Principles

The project follows several engineering principles.

### Modular

Each major capability is isolated behind a clear interface.

### Replaceable

LLMs, embedding models, vector databases, and tools should be replaceable without rewriting the entire system.

### Testable

Core components should be independently testable.

### Observable

Important system behavior should eventually be measurable and traceable.

### Incremental

The platform is built one capability at a time instead of introducing a large framework before understanding its underlying components.

### Production-Oriented

Although the project is also a learning project, the architecture is designed with real-world deployment requirements in mind.

---

# 📌 Project Status

This project is under active development.

The current focus is the **RAG foundation**, which will serve as the knowledge and retrieval layer for the future agent architecture.

The architecture will evolve as new components are implemented.


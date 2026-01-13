# QA-Copilot com RAG

Projeto em desenvolvimento de um **QA-Copilot** baseado em **Retrieval-Augmented Generation (RAG)**, com foco em **geração de casos de teste** e **consulta inteligente de requisitos** utilizando **arquivos de texto puro (.txt)**.

Este repositório está sendo desenvolvido de forma incremental, com objetivos **acadêmicos (nível mestrado)** e **aplicação prática** no contexto de Quality Assurance.

---

## Objetivo

Explorar e implementar técnicas modernas de IA aplicada para apoiar atividades de QA, mantendo uma arquitetura simples, reprodutível e focada no aprendizado.

---

## Status

**Projeto em desenvolvimento (MVP em construção)**

---

## Estrutura Inicial



qa-copilot
├── data
│ └── docs # Arquivos .txt (artefatos de QA)
├── src
│ ├── ingestion
│ ├── embeddings
│ ├── retrieval
│ └── generation
├── db # Banco vetorial (não versionado)
├── main.py
└── README.md


---

## Tecnologias (iniciais)

- Python 3.11+
- PyTorch
- Sentence-Transformers
- FAISS ou ChromaDB

---

## Próximos Passos

- Implementar ingestão de arquivos `.txt`
- Criar pipeline inicial de embeddings
- Definir prompt base para QA
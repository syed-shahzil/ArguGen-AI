<div align="center">
  <img src="https://img.shields.io/badge/Python-3.13+-blue.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/UI-Gradio-orange.svg?style=for-the-badge&logo=appveyor&logoColor=white" alt="Gradio">
  <img src="https://img.shields.io/badge/Database-PostgreSQL-blue.svg?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  
  <h1>🌌 ArguGen_AI</h1>
  <p><strong>The Premier AI-Powered Real-Time Debate & Evaluation Arena</strong></p>
  <p>Developed by <b>Syed Shahzil</b>, <i>AI Engineer</i> 🦾</p>
</div>

---

## 🎞️ System Demonstration

*A practical look at how ArguGen_AI conducts real-time LLM debates.*

<video src="assets/demo_video.mp4" controls width="100%"></video>

---

## 🧬 Core Overview

**ArguGen_AI** is an advanced interactive platform that pits state-of-the-art Large Language Models against one another to rigorously debate complex statements. 

This head-to-head debating arena has been crafted as the **ultimate evaluation method for LLMs**. Instead of relying on static benchmark datasets, ArguGen_AI forces models to:
- Construct well-reasoned arguments dynamically.
- Respond to opposing viewpoints logically.
- Maintain stylistic and factual consistency across multiple rounds.

At the end of the 3-round debate, a fixed **Judge LLM** evaluates both the *Favor* and *Opposition* frameworks to provide an impartial verdict.

---

## ☄️ Key Capabilities

- **⚡ Token-by-Token Streaming:** Lightning-fast, non-blocking asynchronous Python UI powered by Gradio's streaming generators.
- **🪐 Dynamic Model Switching:** Seamlessly switch between global OpenAI providers (GPT-4o, GPT-3.5-Turbo) and local runtimes (Ollama/Mistral/Llama3.1) entirely from the UI.
- **🔬 Analytical Evaluation:** By placing models in constrained adversarial arenas, you can fundamentally stress-test LLM reasoning loops.
- **🎙️ Speech Synthesis:** Simulates a fully immersive debate with voice synthesis for the Favor, Opposition, and Judge components.
- **🧊 Persistent UI Architecture:** A premium card-based static component UI that renders flawlessly without flickering.

---

## 🦾 Infrastructure Stack

ArguGen_AI features a highly robust and containerized architecture designed for scalability and fast execution.

| Technology | Role |
|------------|------|
| **Python `3.13+`** | Core Language & Logic |
| **Gradio (`v6.9`)** | Real-time Web User Interface |
| **OpenAI & Ollama** | LLM Inference Backends |
| **OpenRouter** | Cloud inference API Gateway |
| **SQLAlchemy** | Backend ORM for State/Logging |
| **PostgreSQL** | Containerized persistence layer via Docker |
| **Poetry Core** | Python Dependency Management |

---

## 🎛️ Deployment Guide

Follow these steps to deploy ArguGen_AI locally.

### 1. Prerequisites
- **Python 3.13+** installed on your system.
- **Poetry** installed (`pip install poetry`).
- **Docker & Docker Compose** installed for the containerized Database.
- Access to **Ollama** locally (optional) and valid **OpenAI / OpenRouter API Keys**.

### 2. Clone the Repository
```bash
git clone https://github.com/syed-shahzil/ArguGen-AI
cd ArguGen_AI
```

### 3. Start the Containerized Database
I use a containerized PostgreSQL instance to manage persistence and state evaluation reliably.
```bash
# From within the repository directory (assuming a docker-compose.yaml is present)
docker-compose up -d
```

### 4. Install Dependencies
ArguGen_AI utilizes `pyproject.toml` managed by Poetry.
```bash
poetry install
```

### 5. Configure Environment Variables
Set your keys for voice engines, OpenRouter, and OpenAI.
```bash
# .env file example:
OPENAI_API_KEY=sk-xxxx...
OLLAMA_URL=http://localhost:11434/api/chat
DATABASE_URL=postgresql://user:pass@localhost:5432/argugen
```

### 6. Launch the Arena
Trigger the Gradio application:
```bash
poetry run python app.py
```
Open the provided `localhost` link in your browser to access the ArguGen_AI Arena.

---

## ⚖️ The Judgement Protocol

Why use ArguGen for evaluating LLMs? 
Standard metrics (MMLU, HumanEval) fail to measure **nuance**, **resilience in conversation**, and **adversarial logic**. ArguGen_AI specifically acts as a red-teaming arena. The fixed Judge LLM ranks both agents based on:
1. Argument validity and cohesion.
2. Refutation of the opposing model's points.
3. Logical fallacies avoided.

---

<div align="center">
  <i>"Evaluating AI, by pitting AI against AI."</i> 🪩
</div>

# Stateful Multi-Agent AI System using LangGraph

An autonomous multi-agent orchestration workflow built with Python, LangGraph, and LangChain that leverages Google's `gemini-2.5-flash` model to process tasks, generate optimized Python scripts, and run autonomous self-correction iterations.

## 🛠️ Tech Stack
- **Framework:** LangGraph, LangChain
- **LLM Core:** Google Gemini API (`gemini-2.5-flash`)
- **Environment Management:** Python-Dotenv

## 🤖 System Architecture & Workflow
The system initializes a structured StateGraph pipeline with distinct operational responsibilities:
1. **Researcher Node:** Extracts user processing intent and formats optimization context guidelines.
2. **Coder Node:** Automatically writes raw, clean Python scripts targeting data requirements.
3. **Reviewer Edge Router (Conditional Gateway):** An autonomous evaluation node that analyzes the output structure. If it encounters missing syntax definitions, it dynamically routes the state thread back to the generator for automated self-correction iterations.
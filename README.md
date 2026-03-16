# AI Notification Assistant
An AI-powered system that collects notifications from different sources, prioritizes them using an LLM, and presents them in a centralized dashboard to reduce notification overload.

## Features
- Email notification ingestion
- AI priority classification (High / Medium / Low)
- Automatic summarization of notifications
- PostgreSQL database storage
- Real-time dashboard using Streamlit
- AI-generated daily summary of notifications

## Tech Stack
- FastAPI (Backend API)
- PostgreSQL (Database)
- LangChain + Groq LLM (AI Processing)
- Streamlit (Dashboard)
- Python

## Architecture
Notification Sources → FastAPI Backend → AI Processing → PostgreSQL → Streamlit Dashboard

## Project Structure

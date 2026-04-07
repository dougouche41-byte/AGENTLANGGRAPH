"""
Cerveau de l'assistant : petit graphe LangGraph qui appelle GPT-4o-mini.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import MessagesState

load_dotenv()

MODEL_NAME = "gpt-4o-mini"

DEFAULT_SYSTEM_PROMPT = (
    "Tu es un assistant utile, patient et clair. "
    "Tu réponds toujours en français, sauf si l'utilisateur écrit dans une autre langue "
    "et semble préférer cette langue."
)


def _require_api_key() -> None:
    if not os.getenv("OPENAI_API_KEY", "").strip():
        raise RuntimeError(
            "Variable d'environnement OPENAI_API_KEY manquante. "
            "Ajoutez-la dans un fichier .env à la racine du projet : OPENAI_API_KEY=sk-..."
        )


def build_graph(system_prompt: str | None = None):
    """Construit le graphe (une entrée → modèle → sortie)."""
    _require_api_key()
    system = (system_prompt or DEFAULT_SYSTEM_PROMPT).strip()
    llm = ChatOpenAI(model=MODEL_NAME, temperature=0.6)

    def call_model(state: MessagesState):
        messages_with_system = [SystemMessage(content=system), *state["messages"]]
        answer = llm.invoke(messages_with_system)
        return {"messages": [answer]}

    graph = StateGraph(MessagesState)
    graph.add_node("agent", call_model)
    graph.add_edge(START, "agent")
    graph.add_edge("agent", END)
    return graph.compile()


_compiled_graph = None


def get_graph():
    """Instance unique du graphe (lazy)."""
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_graph()
    return _compiled_graph


def reset_graph() -> None:
    """Utile pour les tests ou après changement de clé API."""
    global _compiled_graph
    _compiled_graph = None


def reply(history: list[BaseMessage]) -> AIMessage:
    """
    Passe l'historique de conversation (messages utilisateur / assistant)
    et renvoie la prochaine réponse du modèle.
    """
    result = get_graph().invoke({"messages": list(history)})
    last = result["messages"][-1]
    if isinstance(last, AIMessage):
        return last
    return AIMessage(content=str(getattr(last, "content", last)))


def new_user_message(text: str) -> HumanMessage:
    return HumanMessage(content=text.strip())

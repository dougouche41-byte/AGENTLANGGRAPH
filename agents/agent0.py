from utils.llm_wrapper import simple_chain
# from utils.memory import search_memory  # Temporairement désactivé

def agent0_run(user_input: str):
    # 1. TEMPORAIRE : on skip Qdrant pour l'instant
    # memories = search_memory(user_input, limit=3)
    memories = []  # On branche Qdrant après avoir résolu l'auth

    # 2. On prépare les souvenirs pour l'IA
    context_lines = []
    for mem in memories:
        payload = mem.get("payload", {})
        text = payload.get("text") or payload.get("mission") or str(payload)
        context_lines.append(f"- {text}")

    memory_context = "\n".join(context_lines) if context_lines else "Aucun souvenir utile."

    # 3. Le Chef réfléchit en mélangeant la demande actuelle et le passé
    prompt = """
Tu es un chef d'orchestration IA.
Tu transformes la demande utilisateur en mission claire.

Contexte mémoire (ce qui a été fait avant) :
{memory_context}

Demande actuelle de l'utilisateur :
{input}

Réponds avec UNE seule phrase de mission.
"""
    result = simple_chain(prompt, {"input": user_input, "memory_context": memory_context})
    return result.content
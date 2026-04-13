def agent6_run(mission: str):
    """
    Agent 6 = Finance
    Vérifie rapidement si la mission semble acceptable financièrement
    """

    mission_lower = mission.lower()

    alertes = []

    if "10000€" in mission_lower or "10000" in mission_lower:
        alertes.append("Budget potentiellement trop élevé")

    if "urgent" in mission_lower:
        alertes.append("Mission urgente = coût potentiellement plus élevé")

    if alertes:
        return {
            "budget_ok": False,
            "alertes": alertes,
            "resume": "Mission à revoir avant validation financière."
        }

    return {
        "budget_ok": True,
        "alertes": [],
        "resume": "Mission acceptable pour une première analyse financière."
    }
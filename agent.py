from agents.agent0 import agent0_run
from agents.agent6 import agent6_run
from agents.agent8 import agent8_run

def run_agent(user_input: str):
    """
    Pipeline complet multi-agents
    """
    # 1. Le Chef crée la mission
    mission = agent0_run(user_input)

    # 2. La Finance vérifie
    finance = agent6_run(mission)

    # 3. La Mémoire prépare le stockage
    memory = agent8_run(mission)

    return {
        "mission": mission,
        "finance": finance,
        "memory": memory
    }

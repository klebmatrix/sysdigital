def intent_clarification(state):
    return {"clarified_query": state["user_query"]}

def research_brief(state):
    return {"brief": f"Ensinar de forma clara: {state['clarified_query']}"}

def initial_draft(state):
    return {"draft": f"Rascunho educativo sobre {state['brief']}"}

def pedagogical_denoising(state):
    feedback = ["Explicar com exemplos", "Usar linguagem simples"]
    improved = state["draft"] + "\n\nExemplo prático adicionado."
    return {"draft": improved, "feedback": feedback}

def convergence_check(state):
    score = 0.9
    return {"quality_score": score, "approved": score >= 0.85}

def finalize(state):
    return {"final_report": state["draft"]}

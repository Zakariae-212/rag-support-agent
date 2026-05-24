import ollama
from pydantic import BaseModel
from typing import Optional, Literal

MODEL = "qwen3:1.7b"


class ActionDecision(BaseModel):

    action: Literal[
        "repondre",
        "demander_email",
        "creer_ticket",
        "supprimer_ticket"
    ]

    reponse: Optional[str] = None
    email: Optional[str] = None
    priority: Optional[str] = "normal"


def ask_llm(context, question):

    system_prompt = f"""
Tu es un agent support.

Actions possibles :

repondre
demander_email
creer_ticket
supprimer_ticket

Règles :

1. Si la réponse est dans le contexte → repondre
2. Si la réponse n'est pas dans le contexte → demander_email
3. Si l'utilisateur donne un email → creer_ticket
4. Si l'utilisateur veut supprimer ses données ou son ticket → supprimer_ticket

Context:
{context}

Réponds uniquement en JSON valide.
"""

    response = ollama.chat(

        model=MODEL,

        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],

        format=ActionDecision.model_json_schema(),

        options={
            "temperature": 0.0,
            "top_p": 1.0,
            "top_k": 1,
        }
    )

    return ActionDecision.model_validate_json(
        response["message"]["content"]
    )

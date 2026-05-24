from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag import search
from decision import ask_llm
from ticket import create_ticket
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== Schema Request =====
class ChatRequest(BaseModel):
    message: str
    email: str | None = None


# ===== Email validation =====
def is_valid_email(email: str) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


# ===== Endpoint Chat =====
@app.post("/chat")
def chat(req: ChatRequest):

    user_input = req.message

    # 🔥 1️⃣ SI EMAIL FOURNI → créer ticket DIRECTEMENT
    if req.email:
        if is_valid_email(req.email):

            create_ticket(req.email, user_input, "normal")

            return {
                "status": "ticket_created",
                "response": "Votre demande a été enregistrée. Un agent vous contactera."
            }

        return {
            "status": "error",
            "response": "Email invalide."
        }

    # 🔍 2️⃣ SINON → logique normale RAG + LLM
    results = search(user_input)
    context = "\n".join([r["text"] for r in results])

    decision = ask_llm(context, user_input)

    if decision.action == "repondre":
        return {
            "status": "success",
            "response": decision.reponse
        }

    elif decision.action == "demander_email":
        return {
            "status": "need_email",
            "response": "Je ne trouve pas cette information. Veuillez fournir votre email."
        }
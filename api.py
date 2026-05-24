from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag import search
from decision import ask_llm
from ticket import create_ticket, delete_ticket
from database_faq import search_faq, init_faq
from database_tk import init_db
from monitoring import (
    log_faq,
    log_rag,
    log_email,
    log_delete,
    log_time,
    get_metrics
)
import re
import time

app = FastAPI()

init_db()
init_faq()

pending_action = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== Request =====
class ChatRequest(BaseModel):
    message: str
    email: str | None = None


# ===== Email validation =====
def is_valid_email(email: str) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


# ===== CHAT ENDPOINT =====
@app.post("/chat")
def chat(req: ChatRequest):

    user_input = req.message
    global pending_action

    # start timer (C11 metric)
    start_time = time.time()

    # =========================
    # 1️⃣ EMAIL FLOW (ticket / delete)
    # =========================
    if req.email:
        log_email()

        if is_valid_email(req.email):

            if pending_action == "supprimer_ticket":
                delete_ticket(req.email)
                pending_action = None

                log_delete()
                log_time(start_time)

                return {
                    "status": "ticket_deleted",
                    "response": "Vos données ont été supprimées avec succès."
                }

            create_ticket(req.email, user_input, "normal")
            pending_action = None

            log_time(start_time)

            return {
                "status": "ticket_created",
                "response": "Votre demande a été enregistrée. Un agent vous contactera."
            }

        return {
            "status": "error",
            "response": "Email invalide."
        }

    # =========================
    # 2️⃣ SEARCH FAQ (BDD)
    # =========================
    faq_answer = search_faq(user_input)

    if faq_answer:

        print("\n========== FAQ RESPONSE ==========")
        print(faq_answer)
        print("==================================\n")

        log_faq()
        log_time(start_time)

        return {
            "status": "success",
            "response": faq_answer
        }

    # =========================
    # 3️⃣ SEARCH RAG
    # =========================
    log_rag()

    results = search(user_input)
    context = "\n".join([r["text"] for r in results])

    print("\n========== CONTEXT ==========")
    print(context)
    print("=============================\n")

    decision = ask_llm(context, user_input)

    # =========================
    # 4️⃣ LLM DECISION
    # =========================
    log_time(start_time)

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

    elif decision.action == "supprimer_ticket":
        pending_action = "supprimer_ticket"
        return {
            "status": "need_email_delete",
            "response": "Veuillez fournir votre email pour supprimer vos données."
        }
    
@app.get("/metrics")
def metrics_endpoint():
    return get_metrics() 
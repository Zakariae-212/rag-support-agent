from rag import search
from decision import ask_llm
from ticket import create_ticket
import re

def is_valid_email(email: str) -> bool:
    """
    Vérifie si la chaîne donnée est un email valide
    """
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

MAX_TRIES = 3  # nombre d'essais pour saisir un email

last_question = None

while True:
    user_input = input("\nUser: ").strip()
    if not user_input:
        print("Veuillez entrer une question.")
        continue

    # 1️ Recherche RAG
    results = search(user_input)
    context = "\n".join([r["text"] for r in results])

    # 2️ Décision LLM
    decision = ask_llm(context, user_input)

    # 3️ Action selon la décision
    if decision.action == "repondre":
        print("\nAgent:", decision.reponse)

    elif decision.action == "demander_email":
        print("\nAgent: Je ne trouve pas cette information.")
        tries = 0
        while tries < MAX_TRIES:
            email = input("Veuillez fournir votre email : ").strip()
            if is_valid_email(email):
                create_ticket(email, user_input, "normal")
                print("Ticket créé avec succès.")
                break
            else:
                tries += 1
                print(f"Email invalide, veuillez réessayer ({MAX_TRIES - tries} essais restants).")
        if tries == MAX_TRIES:
            print("Nombre maximum d'essais atteint. Le ticket n'a pas été créé.")

    elif decision.action == "creer_ticket":
        if decision.email and is_valid_email(decision.email):
            create_ticket(decision.email, user_input, decision.priority or "normal")
            print("Ticket créé avec succès.")
        else:
            print("Impossible de créer le ticket : email manquant ou invalide.")

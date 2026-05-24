import time
from collections import defaultdict

metrics = {
    "faq": 0,
    "rag": 0,
    "email": 0,
    "delete": 0,
    "response_times": []
}


def log_faq():
    metrics["faq"] += 1


def log_rag():
    metrics["rag"] += 1


def log_email():
    metrics["email"] += 1


def log_delete():
    metrics["delete"] += 1


def log_time(start):
    metrics["response_times"].append(time.time() - start)


def get_metrics():
    return {
        "faq_usage": metrics["faq"],
        "rag_usage": metrics["rag"],
        "email_requests": metrics["email"],
        "delete_requests": metrics["delete"],
        "avg_response_time": (
            sum(metrics["response_times"]) / len(metrics["response_times"])
            if metrics["response_times"] else 0
        )
    }
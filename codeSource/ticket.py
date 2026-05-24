import csv
from datetime import datetime


def create_ticket(email, question, priority):

    with open("tickets.csv", "a", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        writer.writerow([
            email,
            question,
            datetime.now().isoformat(),
            priority
        ])
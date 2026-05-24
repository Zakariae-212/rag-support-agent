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

def delete_ticket(email):

    rows = []

    with open("tickets.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)

        for row in reader:

            if not row:
                continue  # ignore lignes vides

            if len(row) < 4:
                continue  # ignore lignes cassées

            if row[0] != email:
                rows.append(row)

    with open("tickets.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
import sqlite3
from datetime import datetime

DB_NAME = "tickets.db"


def create_ticket(email, question, priority):

    conn = sqlite3.connect(DB_NAME, check_same_thread=False, timeout=10)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tickets (email, question, date, priority)
        VALUES (?, ?, ?, ?)
    """, (email, question, datetime.now().isoformat(), priority))

    conn.commit()
    conn.close()


def delete_ticket(email):

    conn = sqlite3.connect(DB_NAME, check_same_thread=False, timeout=10)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM tickets WHERE email = ?
    """, (email,))

    conn.commit()
    conn.close()
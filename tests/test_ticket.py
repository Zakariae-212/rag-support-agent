import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ticket import create_ticket, delete_ticket
import sqlite3

DB_NAME = "tickets.db"


def test_create_ticket():

    create_ticket(
        "test@test.com",
        "Question test",
        "normal"
    )

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tickets WHERE email=?",
        ("test@test.com",)
    )

    result = cursor.fetchone()

    conn.close()

    assert result is not None


def test_delete_ticket():

    delete_ticket("test@test.com")

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tickets WHERE email=?",
        ("test@test.com",)
    )

    result = cursor.fetchone()

    conn.close()

    assert result is None
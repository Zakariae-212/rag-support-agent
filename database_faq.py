import sqlite3

DB_NAME = "faq.db"


def init_faq():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS faq (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT
    )
    """)

    conn.commit()
    conn.close()


def search_faq(question):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT answer
        FROM faq
        WHERE question LIKE ?
        LIMIT 1
    """, (f"%{question}%",))

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return None
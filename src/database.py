import sqlite3

DB_PATH = "database/chat_history.db"


def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_email TEXT,
            retrieved_doc TEXT,
            ai_reply TEXT,
            status TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_conversation(email, document, reply, status):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO conversations
        (customer_email, retrieved_doc, ai_reply, status)
        VALUES (?, ?, ?, ?)
    """, (email, document, reply, status))

    conn.commit()
    conn.close()


def get_conversations():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT customer_email,
               retrieved_doc,
               ai_reply,
               status
        FROM conversations
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows
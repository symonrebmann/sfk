import sqlite3
from parsing import extract_question_blocks, extract_response_blocks

conn = sqlite3.connect("sfk.db")

cursor = conn.cursor()

def entry_sessions(question_category: str, question_type: str, difficulty: int, today: str) -> int:
    
    question_type = question_type.split(".")[1].strip()
    
    cursor.execute("""
        INSERT INTO sessions (question_category, question_type, difficulty, date)
        VALUES (?, ?, ?, ?)
    """, (question_category, question_type, difficulty, today))

    conn.commit()
    session_id = cursor.lastrowid

    return session_id

def entry_questions(text: str, session_id: int) -> None:
    question_number = 0
    question_blocks = extract_question_blocks(text)
    for block in question_blocks:
        question_number += 1
        question_topic = block["topic"]
        question_text = block["question"]
        cursor.execute("""
            INSERT INTO questions (session_id, question_number, question_topic, question_text)
            VALUES (?, ?, ?, ?)
        """, (session_id, question_number, question_topic, question_text))

    conn.commit()


def entry_responses(text: str, session_id: int) -> None:
    response_blocks= extract_response_blocks(text)

    question_ids = []

    cursor.execute("""
        SELECT id FROM questions           
        WHERE session_id = ?            
        ORDER BY question_number           
        """, (session_id,))
    
    for row in cursor.fetchall():
        question_ids.append(row[0])

    for block, question_id in zip(response_blocks, question_ids):
        answer = block["answer"]
        grade = block["grade"]
        explanation = block["explanation"]
        cursor.execute("""
            INSERT INTO responses (question_id, answer, grade, explanation)
            VALUES (?, ?, ?, ?)
        """, (question_id, answer, grade, explanation))
    
    conn.commit()

def entry_session_subjects(text: list[str], session_id: int) -> None:

    for item in text:
        cursor.execute("""
            INSERT INTO session_subjects (session_id, subject)
            VALUES (?, ?)
        """, (session_id, item))

    conn.commit()

def initiate_db() -> None:

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY,
            question_category TEXT,
            question_type TEXT,
            difficulty INTEGER,
            date TEXT
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY,
            session_id INTEGER,
            question_number INTEGER,
            question_topic TEXT,
            question_text TEXT,
            FOREIGN KEY (session_id) REFERENCES sessions(id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY,
            question_id INTEGER,
            answer TEXT,
            grade TEXT,
            explanation TEXT,
            FOREIGN KEY (question_id) REFERENCES questions(id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS session_subjects (
        id INTEGER PRIMARY KEY,
        session_id INTEGER,
        subject TEXT,
        FOREIGN KEY (session_id) REFERENCES sessions(id)
        );
    """)

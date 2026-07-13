from db.database import get_db
from db.queries import (
    INSERT_QUESTION,
    GET_ALL_QUESTIONS,
    DELETE_QUESTION,
    GET_QUESTION_BY_ID, 
    QUESTION_EXISTS
)

def get_all_questions():
    conn = get_db()
    questions = conn.execute(GET_ALL_QUESTIONS).fetchall()
    conn.close()
    return [dict(i) for i in questions]

def get_question_by_id(id):
    conn = get_db()
    question = conn.execute(GET_QUESTION_BY_ID, (id, )).fetchone()
    conn.close()
    return dict(question) if question else None


def add_question(text: str, answer: str):
    conn = get_db()
    question_id = conn.execute(INSERT_QUESTION, (text, answer)).fetchone()
    conn.commit()
    conn.close()
    return dict(question_id) if question_id else None

def delete_question(id):
    conn = get_db()
    conn.execute(DELETE_QUESTION, (id,))
    conn.commit()
    conn.close()

def if_exists(question_text):
    conn = get_db()
    exists = conn.execute(QUESTION_EXISTS, (question_text, )).fetchone
    conn.commit()
    conn.close()
    return bool(exists)


import sqlite3

from config import DATABASE
from src.questions import QUESTIONS
from db.queries import (
    CREATE_QUESTIONS_TABLE,
    CREATE_RESULTS_TABLE,
    CREATE_USERS_TABLE,
    INSERT_QUESTION,
    GET_ALL_QUESTIONS
)


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row     # строки возвращает как словари
    return conn


def init_db():
    conn = get_db()
    conn.execute(CREATE_USERS_TABLE)
    conn.execute(CREATE_QUESTIONS_TABLE)
    conn.execute(CREATE_RESULTS_TABLE)
    if not conn.execute(GET_ALL_QUESTIONS).fetchall():
        for q_text, q_answer in QUESTIONS:
            conn.execute(INSERT_QUESTION, (q_text, q_answer))    
    conn.commit()
    conn.close()
    

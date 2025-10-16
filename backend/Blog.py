from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import pandas as pd

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_path = 'blog.db'
class Post(BaseModel):
    login: str
    content: str
def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blog (
        login TEXT NOT NULL,
        content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.post('/Getdb')
def get_db():
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("Select * from blog", conn)
    conn.close()
    return {'user' : df['login'].tolist(), 'content' : df['content'].tolist()}

@app.post('/Add')
def add_post(post : Post):
    conn = sqlite3.connect(db_path)
    login = post.login
    content = post.content
    cursor = conn.cursor()
    cursor.execute(""" INSERT INTO blog (login, content) VALUES (?, ?)""", [login, content])
    conn.commit()
    conn.close()
    return get_db()
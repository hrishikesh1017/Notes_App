from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from. import models
from.database import engine
from .routers import note

models.Base.metadata.create_all(bind = engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'notes_app', user = 'postgres', password = 'kannan', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection success')
        break
    except Exception as error:
        print("connection Failed")
        print("error", error)
        time.sleep(2)

app.include_router(note.router)
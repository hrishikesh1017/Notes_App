from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import Response, HTTPException, Depends, APIRouter
from .. import models, schemas
from typing import List
import google.generativeai as genai
import os


os.environ['GOOGLE_API_KEY'] = ""
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

model = genai.GenerativeModel('gemini-pro')

router = APIRouter(
    prefix = '/notes',
    tags = ['Notes']
)

@router.get("/", response_model=List[schemas.Note])
async def get_notes(db:Session = Depends(get_db)):
    posts = db.query(models.Note).all()
    return posts


@router.post("/", status_code=201, response_model=schemas.Note)
def create_posts(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    new_note = models.Note(**note.model_dump())
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


@router.get("/search", response_model=List[schemas.Note])
async def search_notes(context: str, db: Session = Depends(get_db)):
    # Step 1: Fetch all notes from the database
    notes = db.query(models.Note).all()

    # Step 2: Prepare the data for the Gemini API
    notes_content = [note.content for note in notes]
    prompt = f"Find notes that match the context: '{context}'.\n\n" \
             f"Here are the contents of the notes:\n" + "\n\n".join(notes_content)

    # Step 3: Call the Gemini API to filter the notes
    try:
        response = model.generate_content(prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API request failed: {e}")

    # Step 4: Parse the Gemini response to identify matching notes
    matching_notes = []
    gpt_response = response.text.strip()

    # Check if the response contains the content of any notes
    for note in notes:
        if note.content in gpt_response:
            matching_notes.append(note)

    # Step 5: Return the IDs and contents of matching notes
    return matching_notes
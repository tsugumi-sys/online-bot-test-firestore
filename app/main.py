from typing import List
from fastapi import FastAPI, HTTPException

from . import crud, schemas
from .database import get_firestore_db

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/bots/", response_model=schemas.Bot)
def create_bot(bot: schemas.BotCreate):
    db = get_firestore_db()
    bot = crud.create_bot(db, bot)
    if bot is None:
        raise HTTPException(status_code=400, detail="Cannot register this bot.")

    return bot


@app.get("/bots/", response_model=List[schemas.Bot])
def read_bots():
    db = get_firestore_db()
    bots = crud.get_bots(db)
    return bots


@app.get("/bots/{bot_id}", response_model=schemas.Bot)
def read_bot(bot_id: str):
    db = get_firestore_db()
    bot = crud.get_bot_by_id(db, bot_id)
    if bot is None:
        raise HTTPException(status_code=400, detail="This bot is not Found.")

    return bot


@app.get("/bot_id/", response_model=str)
def read_bot_id(bot: schemas.Bot):
    db = get_firestore_db()
    bot_id = crud.get_bot_id(db, bot)
    if bot_id is None:
        raise HTTPException(status_code=400, detail="Bot is not registered.")

    return bot_id


@app.post("/bots/{bot_id}/records/", response_model=schemas.PredictRecord)
def create_record(bot_id: str, record: schemas.PredictRecordCreate):
    db = get_firestore_db()
    bot = crud.get_bot_by_id(db, bot_id)
    if bot is None:
        raise HTTPException(status_code=400, detail="Invalid 'bot_id'")

    record = crud.create_record(db, bot_id, record)
    if record is None:
        raise HTTPException(status_code=400, detail="Failed to create record to firestore.")

    return record


@app.get("/bots/{bot_id}/records/", response_model=List[schemas.PredictRecord])
def read_records(bot_id: str):
    db = get_firestore_db()
    bot = crud.get_bot_by_id(db, bot_id)
    if bot is None:
        raise HTTPException(status_code=400, detail="Invalid 'bot_id'")

    records = crud.get_records(db, bot_id)
    return records


@app.get("/bots/{bot_id}/records/{record_id}/", response_model=schemas.PredictRecord)
def read_record(bot_id: str, record_id: str):
    db = get_firestore_db()
    bot = crud.get_bot_by_id(db, bot_id)
    if bot is None:
        raise HTTPException(status_code=400, detail="Invalid 'bot_id'")

    record = crud.get_record(db, bot_id, record_id)
    if record is None:
        raise HTTPException(status_code=400, detail="Invalid 'record_id'")

    return record

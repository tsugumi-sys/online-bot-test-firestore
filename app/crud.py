from datetime import datetime
from typing import Dict, Optional, List
from google.cloud.firestore import Client

from . import schemas


def create_bot(db: Client, bot: schemas.BotCreate) -> Optional[schemas.Bot]:
    bot_ref = db.collection("bot").add(bot.dict())

    bot_id: str = bot_ref[1].id
    created_bot = get_bot_by_id(db, bot_id)
    if created_bot is None:
        return None
    else:
        return created_bot


def remove_bot(db: Client, bot_id: str) -> Optional[str]:
    deleted_timestamp: datetime = db.collection("bot").document(bot_id).delete()
    return datetime.strftime(deleted_timestamp, "%d/%m/%Y %H:%M:%S")


def get_bot_id(db: Client, bot: schemas.BotBase) -> Optional[str]:
    bot_ref: list = (
        db.collection("bot")
        .where("name", "==", bot.name)
        .where("version", "==", bot.version)
        .where("exchange_name", "==", bot.exchange_name)
        .where("trading_type", "==", bot.trading_type)
        .where("pair_name", "==", bot.pair_name)
        .get()
    )

    if len(bot_ref) == 0:
        return None
    else:
        return bot_ref[0].id


def get_bot_by_id(db: Client, bot_id: str) -> Optional[schemas.Bot]:
    db_bot = db.collection("bot").document(bot_id).get()
    if db_bot.exists:
        return schemas.Bot(**db_bot.to_dict(), bot_id=bot_id)
    else:
        return None


def get_bots(db: Client) -> List[schemas.Bot]:
    bots = db.collection("bot").stream()

    return [schemas.Bot(**i.to_dict(), bot_id=i.id) for i in bots]


def create_record(db: Client, bot_id: str, record: schemas.RecordCreate) -> Optional[schemas.Record]:
    record_ref = db.collection(bot_id).add(record.dict())

    record_id: str = record_ref[1].id
    created_record = get_record(db, bot_id, record_id)

    if created_record is None:
        return None
    else:
        return created_record


def remove_record(db: Client, bot_id: str, record_id: str) -> Dict:
    deleted_timestamp: datetime = db.collection(bot_id).document(record_id).delete()
    return datetime.strftime(deleted_timestamp, "%d/%m/%Y %H:%M:%S")


def remove_records(db: Client, bot_id: str, batch_size: int = 100):
    all_records = db.collection(bot_id).limit(batch_size).stream()
    deleted_count: int = 0

    for record in all_records:
        record.reference.delete()
        deleted_count += 1

    if deleted_count >= batch_size:
        return remove_records(db, bot_id, batch_size)

    return {"deleted_records": deleted_count}


def get_record(db: Client, bot_id: str, record_id: str) -> Optional[schemas.Record]:
    record = db.collection(bot_id).document(record_id).get()
    if record.exists:
        return schemas.Record(**record.to_dict(), bot_id=bot_id, record_id=record_id)
    else:
        return None


def get_records(db: Client, bot_id: str) -> List:
    record_ref = db.collection(bot_id).stream()
    return [schemas.Record(**i.to_dict(), bot_id=bot_id, record_id=i.id) for i in record_ref]

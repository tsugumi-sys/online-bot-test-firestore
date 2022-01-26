from typing import Optional, List
from google.cloud.firestore import Client

from . import schemas


def get_bot_id(db: Client, bot: schemas.Bot) -> Optional[str]:
    bot = bot.dict()
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
        return schemas.Bot(**db_bot.to_dict())
    else:
        return None


def get_bots(db: Client) -> List:
    bots = db.collection("bot").stream()
    return [i.to_dict() for i in bots]


def create_bot(db: Client, bot: schemas.BotCreate) -> Optional[schemas.Bot]:
    bot_ref = db.collection("bot").add(bot.dict())

    bot_id: str = bot_ref[1].id
    created_bot = get_bot_by_id(db, bot_id)
    if created_bot is None:
        return None
    else:
        return created_bot


def get_record(db: Client, bot_id: str, record_id: str) -> Optional[schemas.PredictRecord]:
    record = db.collection(bot_id).document(record_id).get()
    if record.exists:
        return schemas.PredictRecord(**record.to_dict())
    else:
        return None


def get_records(db: Client, bot_id: str) -> List:
    record_ref = db.collection(bot_id).stream()
    return [i.to_dict() for i in record_ref]


def create_record(db: Client, record: schemas.PredictRecordCreate, bot_id: str) -> Optional[schemas.PredictRecord]:
    record_ref = db.collection(bot_id).add(record.dict())

    record_id: str = record_ref[1].id
    created_record = get_record(db, bot_id, record_id)

    if created_record is None:
        return None
    else:
        return created_record

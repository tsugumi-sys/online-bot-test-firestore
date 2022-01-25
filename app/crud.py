from typing import Optional, List
from firebase_admin.firestore import client

from . import schemas


def get_bot(db: client, bot_id: str) -> Optional[schemas.Bot]:
    db_bot = db.collection("bot").document(bot_id).get()
    if db_bot.exists:
        return db_bot.to_dict()
    else:
        return None


def get_bots(db: client) -> List:
    bots = db.collection("bot").stream()
    return [d.to_dict() for d in bots]

from typing import Dict
from datetime import datetime

from pydantic import BaseModel


class BotBase(BaseModel):
    # Id is created from firestore.client().document("bot").add()
    name: str
    version: str
    exchange_name: str
    trading_type: str
    pair_name: str


class BotCreate(BotBase):
    pass


class Bot(BotBase):
    bot_id: str


class RecordBase(BaseModel):
    # Id is created from firestore.client().document(bot_id).add()
    timestamp: datetime  # In requests and responses will be represented as a str in ISO 8601 format, like: 2008-09-15T15:53:00+05:00.
    buy_predict_value: float
    sell_predict_value: float
    buy_limit_price: float
    sell_limit_price: float
    close: float
    other_item: Dict


class RecordCreate(RecordBase):
    pass


class Record(RecordBase):
    bot_id: str
    record_id: str

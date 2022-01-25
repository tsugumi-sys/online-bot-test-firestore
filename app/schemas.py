from datetime import datetime

from pydantic import BaseModel


class BotBase(BaseModel):
    # Id is created from firestore.client().add()
    name: str
    version: str
    exchange_name: str
    trading_type: str
    pair_name: str


class BotCreate(BotBase):
    pass


class Bot(BotBase):
    pass


class PredictRecordBase(BaseModel):
    # id does not used bacause firestore.client().set()
    bot_id: str
    timstamp: datetime
    predict_value: float
    open: float
    high: float
    low: float
    close: float
    volume: float


class PredictRecord(PredictRecordBase):
    pass


class PredictRecordCreate(PredictRecordBase):
    pass

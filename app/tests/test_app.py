from datetime import datetime
from typing import List, Tuple
from requests import Response
import unittest
from fastapi.testclient import TestClient

from ..schemas import BotCreate, Bot, Record, RecordCreate
from ..main import app, delete_record

unittest.TestLoader.sortTestMethodsUsing = None


class TestApp(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.client = TestClient(app)

        self.test_bot = BotCreate(
            name="test_bot",
            version="test_Ver",
            exchange_name="test_exchange",
            trading_type="test_trading_type",
            pair_name="test_pair_name",
        )

        # Delete if test_bot is exits
        # If error occured while doing tests, the test_bot data may remain in firestore.
        res = self.client.get("/bot_id/", params=self.test_bot.dict())
        if res.status_code == 200:
            bot_id: str = res.json()
            # Delete record if exists
            _ = self.client.delete("/bots/", params={"bot_id": bot_id})

        self.test_record = RecordCreate(
            timestamp=datetime.now(),
            buy_predict_value=1.0,
            sell_predict_value=1.0,
            buy_limit_price=200.0,
            sell_limit_price=199.0,
            close=1000.0,
        )

    # Test helper functions
    def create_test_bot(self) -> Bot:
        res = self.client.post("/bots/", json=self.test_bot.dict())
        bot = res.json()
        return Bot(**bot)

    def remove_test_bot(self, bot_id: str) -> Response:
        res = self.client.delete("/bots/", params={"bot_id": bot_id})
        return res

    def create_test_bot_and_record(self) -> Tuple[Bot, Record]:
        bot = self.create_test_bot()
        bot_id: str = bot.bot_id

        res = self.client.post("/bots/{bot_id}/records", params={"bot_id": bot_id, "record": self.test_record.dict()})
        print(res.status_code)
        record = res.json()

        return bot, Record(**record)

    def remove_test_bot_and_record(self, bot_id: str, record_id: str) -> Tuple[Response, Response]:
        delete_record_res = self.client.delete("/bots/{bot_id}/records/", params={"bot_id": bot_id, "record_id": record_id})
        delete_bot_res = self.remove_test_bot(bot_id)
        return delete_bot_res, delete_record_res

    # Tests
    def test_helper_functions(self):
        # Test create_test_bot
        bot = self.create_test_bot()
        self.assertIsInstance(bot, Bot)

        # Test remove_test_bot
        res = self.remove_test_bot(bot.bot_id)
        self.assertEqual(res.status_code, 200)

        # Test create_test_bot_and_record
        bot, record = self.create_test_bot_and_record()
        self.assertIsInstance(bot, Bot)
        self.assertIsInstance(record, Record)
        self.assertEqual(bot.bot_id, record.bot_id)

        # # Test remove_test_bot_and_record
        # delete_bot_res, delete_record_res = self.remove_test_bot_and_record(bot.bot_id, record.record_id)
        # self.assertEqual(delete_bot_res.status_code, 200)
        # self.assertEqual(delete_record_res.status_code, 200)

    # def remove_test_bot_and_record(self, bot_id: str, record_id: str) -> None:
    #     _ = self.client.delete("/bots/{bot_id}/records/{record_id}/", params={"bot_id": bot_id, "record_id": record_id})

    # def test_read_bots(self):
    #     # Read bots
    #     res = self.client.get("/bots/")
    #     bots = res.json()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertIsInstance(bots, List)

    # def test_read_bot(self):
    #     # Read bot that doenst exist throws 400 error
    #     res = self.client.get("/bots/{bot_id}", params={"bot_id": "NotExistID"})

    #     self.assertEqual(res.status_code, 400)

    #     # Create bot and get its id
    #     _ = self.client.post("/bots/", json=self.test_bot.dict())
    #     res = self.client.get("/bot_id/", params=self.test_bot.dict())
    #     bot_id: str = res.json()

    #     # Read the created bot
    #     res = self.client.get("/bots/{bot_id}", params={"bot_id": bot_id})

    #     self.assertEqual(res.status_code, 400)
    #     self.assertEqual(res.json(), self.test_bot.dict())

    #     # Delete bot
    #     _ = self.client.delete("/bots/", params={"bot_id": bot_id})

    # def test_read_bot_id(self):
    #     # Get bot_id of uncreated bot throw 400 error.
    #     res = self.client.get("/bot_id/", params=self.test_bot.dict())

    #     self.assertEqual(res.status_code, 400)

    #     # Create bot
    #     _ = self.client.post("/bots/", json=self.test_bot.dict())

    #     # Read bot id
    #     res = self.client.get("/bot_id/", params=self.test_bot.dict())
    #     bot_id: str = res.json()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertIsInstance(bot_id, str)

    #     # Delete bot
    #     _ = self.client.delete("/bots/", params={"bot_id": bot_id})

    # def test_create_bot(self):
    #     # Create bot
    #     res = self.client.post("/bots/", json=self.test_bot.dict())

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(res.json(), self.test_bot.dict())

    #     # Recreating the same bot throws 400 res.
    #     res = self.client.post("/bots/", json=self.test_bot.dict())

    #     self.assertEqual(res.status_code, 400)

    #     # Delete bot.
    #     bot_id = self.client.get("/bot_id/", params=self.test_bot.dict())
    #     bot_id: str = bot_id.json()
    #     _ = self.client.delete("/bots/", params={"bot_id": bot_id})

    # def test_delete_bot(self):
    #     # Deleting a bot of a id that doesn't exsist throws 400 error.
    #     res = self.client.delete("/bots/", params={"bot_id": "NotExistID"})

    #     self.assertEqual(res.status_code, 400)

    #     # Create bot
    #     _ = self.client.post("/bots/", json=self.test_bot.dict())

    #     # Delete bot
    #     bot_id = self.client.get("/bot_id/", params=self.test_bot.dict())
    #     bot_id: str = bot_id.json()
    #     res = self.client.delete("/bots/", params={"bot_id": bot_id})

    #     self.assertEqual(res.status_code, 200)
    #     self.assertIsInstance(res.json(), str)


if __name__ == "__main__":
    unittest.main()

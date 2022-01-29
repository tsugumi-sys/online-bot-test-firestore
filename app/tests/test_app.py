import unittest
from fastapi.testclient import TestClient

from ..schemas import Bot, PredictRecord
from ..main import app


class TestApp(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.client = TestClient(app)

        self.test_bot = Bot(
            name="test_bot",
            version="test_Ver",
            exchange_name="test_exchange",
            trading_type="test_trading_type",
            pair_name="test_pair_name",
        )

    def test_create_bot(self):
        print(self.test_bot.dict())
        response = self.client.post("/bots/", json=self.test_bot.dict())

        print(response.text)


if __name__ == "__main__":
    unittest.main()

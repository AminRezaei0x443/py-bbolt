import unittest
from bbolt import BoltDB


class DBTests(unittest.TestCase):
    def setUp(self):
        self.db = BoltDB()
        self.db.open("./x.db")

    def test_rw(self):
        self.db.put("bucket-1", "k1", "f-x")
        k = self.db.get("bucket-1", "k1").decode("utf-8") 
        assert k == "f-x"
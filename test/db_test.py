import unittest
from bbolt import BoltDB
from tempfile import mkstemp
import os


class DBTests(unittest.TestCase):
    def setUp(self):
        self.db = BoltDB()
        fd, self.path = mkstemp()
        os.close(fd)
        self.db.open(self.path)

    def test_rw(self):
        self.db.put("bucket-1", "k1", "f-x")
        k = self.db.get("bucket-1", "k1").decode("utf-8") 
        assert k == "f-x"
    
    def addCleanup(self, *arg, **kwargs) -> None:
        os.remove(self.path)
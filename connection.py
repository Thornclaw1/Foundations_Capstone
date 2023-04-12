import sqlite3 as sql

class Connection:
    _conn = None
    
    def __init__(self, db_path):
        if self._conn is None:
            self._conn = sql.connect(db_path)
        self.cursor = self._conn.cursor()
    
    def __del__(self):
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def commit(self):
        self._conn.commit()
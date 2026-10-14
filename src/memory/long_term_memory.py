import sqlite3
import json


class LongTermMemory:

    def __init__(self, 
                 db_path="memory.db"):
        
        self.db_path = db_path
        self._initialize()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _initialize(self):
        with self._connect() as conn:
            conn.execute("""
                            CREATE TABLE IF NOT EXISTS memories (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id TEXT NOT NULL,
                            content TEXT NOT NULL,
                            metadata TEXT)
                        """)

    def add(self,
             user_id, 
             content, 
             metadata=None):
        
        with self._connect() as conn:
            conn.execute(
                """
                    INSERT INTO memories
                        (user_id, content, metadata)
                    VALUES (?, ?, ?)
                """,
                (user_id,
                 content,
                 json.dumps(metadata or {})))

    def search(self, 
               user_id,  
               limit=20):
        

        with self._connect() as conn:
            rows = conn.execute("""
                                    SELECT content, metadata
                                    FROM memories
                                    WHERE user_id = ?
                                    ORDER BY id DESC
                                    LIMIT ?
                                """,
                (user_id, 
                 limit)).fetchall()

        return [{"content": content,
                 "metadata": json.loads(metadata or "{}")}
                 for content, metadata in rows]
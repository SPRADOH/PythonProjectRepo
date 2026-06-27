import sqlite3
from datetime import datetime
from config import DATABASE_FILE

class Database:
    """Handles all database operations for the bot"""
    
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_FILE)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        """Create necessary tables if they don't exist"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                task TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                done INTEGER DEFAULT 0
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                message TEXT NOT NULL,
                reminder_time TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def add_todo(self, user_id, task):
        """Add a new todo task"""
        self.cursor.execute(
            "INSERT INTO todos (user_id, task) VALUES (?, ?)",
            (user_id, task)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_todos(self, user_id):
        """Get all incomplete todos for a user"""
        self.cursor.execute(
            "SELECT id, task, created_at FROM todos WHERE user_id = ? AND done = 0",
            (user_id,)
        )
        return self.cursor.fetchall()
    
    def complete_todo(self, todo_id, user_id):
        """Mark a todo as completed"""
        self.cursor.execute(
            "UPDATE todos SET done = 1 WHERE id = ? AND user_id = ?",
            (todo_id, user_id)
        )
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def delete_todo(self, todo_id, user_id):
        """Delete a todo"""
        self.cursor.execute(
            "DELETE FROM todos WHERE id = ? AND user_id = ?",
            (todo_id, user_id)
        )
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def close(self):
        """Close database connection"""
        self.conn.close()
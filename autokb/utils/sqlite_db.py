import sqlite3
import json
from typing import Any, Dict

DATABASE_FILE = "autokb_data.db"

def initialize_db():
    """Initialize the SQLite database and create necessary tables."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tool_responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT NOT NULL,
        query TEXT NOT NULL,
        tool_name TEXT NOT NULL,
        response TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS agent_states (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        state_data TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()

def save_tool_response(topic: str, query: str, tool_name: str, response: Dict[str, Any]):
    """Save a tool's response as JSON in the SQLite database."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO tool_responses (topic, query, tool_name, response)
    VALUES (?, ?, ?, ?)
    ''', (topic, query, tool_name, json.dumps(response)))
    conn.commit()
    conn.close()

def get_tool_responses(topic: str, tool_name: str = None) -> Dict[str, Any]:
    """Retrieve all responses for a given topic, optionally filtered by tool."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    if tool_name:
        cursor.execute('''
        SELECT response FROM tool_responses
        WHERE topic = ? AND tool_name = ?
        ''', (topic, tool_name))
    else:
        cursor.execute('''
        SELECT response FROM tool_responses
        WHERE topic = ?
        ''', (topic,))
    rows = cursor.fetchall()
    conn.close()

    return [json.loads(row[0]) for row in rows]

def save_agent_state(state: Dict[str, Any]):
    """Save an agent's state as JSON in the SQLite database."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO agent_states (state_data)
    VALUES (?)
    ''', (json.dumps(state),))
    conn.commit()
    conn.close()

def get_latest_agent_state() -> Dict[str, Any]:
    """Retrieve the latest agent state from the SQLite database."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT state_data FROM agent_states
    ORDER BY timestamp DESC LIMIT 1
    ''')
    row = cursor.fetchone()
    conn.close()

    return json.loads(row[0]) if row else {}

def clear_tool_responses():
    """Clear all tool responses from the database."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tool_responses')
    conn.commit()
    conn.close()

def remove_tool_response(id: int):
    """Remove a specific tool response by ID."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tool_responses WHERE id = ?', (id,))
    conn.commit()
    conn.close()

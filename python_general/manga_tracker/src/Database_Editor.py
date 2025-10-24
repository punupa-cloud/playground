import sqlite3
import response_pb2 as response_pb
from Tracker import Mtracker
from pathlib import Path
# Build path to the database
BASE_DIR = Path(__file__).resolve().parent.parent  # manga_tracker/ folder
DB_PATH = BASE_DIR / "data" / "manga_tracker.db"

def add(manga_name, manga_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO manga (title, latest_chapter, manga_id) VALUES (?, ?, ?)
    ''', (manga_name, '0', manga_id))
    conn.commit()
    conn.close()


def remove(manga_name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        DELETE FROM manga WHERE title = ?
    ''', (manga_name,))
    conn.commit()
    conn.close()

def list_manga():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT rowid, * FROM manga
    ''')
    mangas = c.fetchall()
    conn.close()
    print(mangas)

def update(tracker):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    latest_db_chapter = c.execute('''
        Select latest_chapter From manga Where rowid = ?
    ''', (tracker.manga_key,)).fetchone()[0]

    if tracker.latest_chapter != latest_db_chapter:
        tracker.new_chapter = True
        c.execute('''
            Update manga Set latest_chapter = ? Where rowid = ?
        ''', (tracker.latest_chapter, tracker.manga_key))
    else:
        tracker.new_chapter = False
    conn.commit()
    conn.close()


def get_manga_id(manga_key):

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    manga_id = c.execute('''
        SELECT manga_id FROM manga Where rowid = ?
    ''', (manga_key,)).fetchone()[0]

    conn.close()
  
    return manga_id


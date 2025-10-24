import sqlite3
import threading
from queue import Queue
from Tracker import Mtracker
from Mailing_Service import send_email
from Manga_Tracker_Thread import sequence
from pathlib import Path


if __name__ == "__main__":

    # Build path to the database
    BASE_DIR = Path(__file__).resolve().parent.parent  # manga_tracker/ folder
    DB_PATH = BASE_DIR / "data" / "manga_tracker.db"

    # Database Creation
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS manga (
            title TEXT NOT NULL,
            latest_chapter TEXT DEFAULT '0',
            manga_id TEXT NULL
        )
    ''') # Added another column manually for manga_id
    conn.commit()

    # Thread section for getting info and updating db
    manga_queue = Queue()
    dblock = threading.Lock()
    threads = []

    for manga_key in c.execute('SELECT rowid FROM manga').fetchall():
        manga_key = int(manga_key[0])
        thread = threading.Thread(target=sequence, args=(manga_key, dblock, manga_queue))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    
    conn.close()

    '''Checking manga_queue contents
    for tracker in list(manga_queue.queue):
        print("Manga name: "+tracker.manga_name +", Latest chapter: "+ tracker.latest_chapter + ", new chapter?: " + str(tracker.new_chapter))
    #'''

    # Calling Mailing Service if new chapter found
    for tracker in list(manga_queue.queue):
        if tracker.new_chapter:
            send_email(manga_queue)
            #print ("Mail Service called")
            break


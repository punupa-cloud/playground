from Tracker import Mtracker
from Data_Scanner import track
from Database_Editor import update

def sequence(manga_key, dblock, manga_queue):
    #Get new info
    tracker = track(manga_key)

    #Update DB
    with dblock:
        update(tracker)
    
    #Add to queue for mailing service
    manga_queue.put(tracker)




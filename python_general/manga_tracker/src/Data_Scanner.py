from Tracker import Mtracker
import requests 
import response_pb2 as response_pb
from Database_Editor import get_manga_id,add

def track(manga_key):
    
    manga_id = get_manga_id(manga_key)
    
    if manga_id is None:
        return None
    
    url = "https://jumpg-webapi.tokyo-cdn.com/api/title_detailV3"
    params = {"lang": "eng", "title_id": manga_id}
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        # Parse protobuf
        response_obj = response_pb.Response()
        response_obj.ParseFromString(response.content)
        
        detail = response_obj.success.manga_detail
        
        # Get latest chapter
        if len(detail.chapters[-1].last_chapter_list) > 0:
            latest_chapter_list = detail.chapters[-1].last_chapter_list
        else:
            latest_chapter_list = detail.chapters[-1].first_chapter_list
        
        latest_chapter = latest_chapter_list[-1]
        
        # Create tracker object
        tracker = Mtracker(
            manga_name=detail.manga.manga_name,
            manga_key=manga_key,
            latest_chapter=latest_chapter.chapter_number.lstrip("#").replace("-", "."),
            new_chapter=False,  # Will be set by update() in Database_Editor
            latest_chapter_url=f"https://mangaplus.shueisha.co.jp/viewer/{latest_chapter.chapter_id}"
        )
        
        return tracker
    else:
        print(f"Failed to fetch data for manga_key {manga_key}. Status code: {response.status_code}")
        return None

import smtplib
import time

def send_email(manga_queue):
    day = time.strftime('%A').lower()
    sender = "pythonmangatracker@gmail.com"
    receiver = "puchanapai@outlook.com"
    password = "ruuperxfgsxeifqw"
    subject = f"Manga Tracker - Weekly Update - {day.capitalize()}"
    body = f"Here are the latest updates on the weekly manga for {day}:"
    
    for manga in manga_queue.queue:
        if manga.new_chapter:
            body = body + f"\nNew chapter available for {manga.manga_name}: Chapter {manga.latest_chapter}\nRead it here: {manga.latest_chapter_url}\n"
        else:
            body = body + f"\nNo new chapter for {manga.manga_name}. The latest chapter is still Chapter {manga.latest_chapter}\nRead it here: {manga.latest_chapter_url}.\n"

    message = f"""From: {sender}
To: {receiver}
Subject: {subject}
Content-Type: text/plain; charset="utf-8"

{body}
"""

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, message.encode('utf-8'))
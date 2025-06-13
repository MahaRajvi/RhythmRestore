import time
import sqlite3
from send_sms import send_sms
from datetime import datetime

def get_all_users():
    conn = sqlite3.connect('data/rhythm_restore.db')
    cursor = conn.cursor()
    cursor.execute('SELECT phone FROM users')
    phones = [row[0] for row in cursor.fetchall()]
    conn.close()
    return phones

while True:
    now = datetime.now()
    current_hour = now.hour
    current_minute = now.minute

    phones = get_all_users()

    # Lunch reminder at 1 PM
    if current_hour == 13 and current_minute == 0:
        for phone in phones:
            send_sms(phone, "🍱 Reminder: Have a healthy lunch! Balance your meals.")

    # Stress break reminder at 5 PM
    if current_hour == 17 and current_minute == 0:
        for phone in phones:
            send_sms(phone, "🧘 Reminder: Take a 5-min stress break! Stretch and breathe.")

    # Sleep preparation reminder at 9 PM
    if current_hour == 21 and current_minute == 0:
        for phone in phones:
            send_sms(phone, "🌙 Reminder: Prepare for good sleep! Reduce screens and relax your mind.")

    time.sleep(60)  # check every 1 minute

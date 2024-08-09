import datetime
import random


def get_word_today(entries):
    if not entries:
        return None

    today = datetime.date.today()
    entry_today = entries.filter(last_selected=today).first()

    if not entry_today:
        entry_today = random.choice(entries.all())
        entry_today.last_selected = today
        entry_today.save()

    return entry_today
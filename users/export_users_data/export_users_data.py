import csv
import os
from django.utils import timezone
from django.contrib.auth.models import User

from translate.models import Entry, Translation


script_dir = os.path.dirname(os.path.realpath(__file__))


def export():
    users = (
        User.objects.filter(is_active=True).filter(is_staff=False).order_by("last_name")
    )

    data = []
    for user in users:
        total_session_duration = 0
        for login_session in user.login_session.all():
            if login_session.logout_at:
                session_duration = (
                    login_session.logout_at - login_session.login_at
                ).total_seconds()
            else:
                session_duration = (
                    timezone.now() - login_session.login_at
                ).total_seconds()

            total_session_duration += session_duration

        entries = Entry.objects.filter(user=user)

        num_entries = entries.count()
        word_count_entries = 0
        list_correctness_entries = []

        for entry in entries:
            word_count_entries += entry.word_count
            list_correctness_entries.append(entry.correctness)

        if list_correctness_entries:
            correctness_entries = (
                sum(list_correctness_entries) / len(list_correctness_entries)
            ) / 100
            correctness_entries = round(correctness_entries, 2)
        else:
            correctness_entries = 0

        translations = Translation.objects.filter(user=user)

        num_translations = translations.count()
        word_count_translations = 0
        list_correctness_translations = []
        num_upvotes = 0
        num_downvotes = 0

        for translation in translations:
            word_count_translations += translation.word_count
            list_correctness_translations.append(translation.correctness)
            num_upvotes += translation.upvote_count()
            num_downvotes += translation.downvote_count()

        if list_correctness_translations:
            correctness_translations = (
                sum(list_correctness_translations) / len(list_correctness_translations)
            ) / 100
            correctness_translations = round(correctness_translations, 2)
        else:
            correctness_translations = 0

        row = {
            "username": user.username,
            "last_name": user.last_name,
            "first_name": user.first_name,
            "email": user.email,
            "date_joined": user.date_joined.date(),
            "login_count": user.profile.login_count,
            "total_session_duration": total_session_duration,
            "reputation": user.profile.reputation,
            "num_entries": num_entries,
            "word_count_entries": word_count_entries,
            "correctness_entries": correctness_entries,
            "num_translations": num_translations,
            "word_count_translations": word_count_translations,
            "correctness_translations": correctness_translations,
            "num_bookmarks": user.bookmarks.count(),
            "num_upvotes": num_upvotes,
            "num_downvotes": num_downvotes,
        }
        data.append(row)

    with open(os.path.join(script_dir, "users_data.csv"), "w") as out_file:
        writer = csv.DictWriter(out_file, fieldnames=list(data[0].keys()))

        writer.writeheader()

        writer.writerows(data)

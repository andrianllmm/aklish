from django.db.models import Count


def sort_entries(entries, sort_by):
    match sort_by:
        case "latest":
            return entries.order_by("-modified_at")
        case "top":
            return entries.annotate(num_bookmarks=Count("bookmarks")).order_by("-num_bookmarks")
        case "reputable":
            return entries.order_by("-user__profile__reputation")
        case "proofread":
            return entries.order_by("-correctness")
        case "translated":
            return (
                entries.annotate(num_translations=Count("translations"))
                .filter(translations__isnull=False)
                .distinct()
                .order_by("-num_translations", "-modified_at")
            )
        case "untranslated":
            return (
                entries.filter(translations__isnull=True)
                .distinct()
                .order_by("-modified_at")
            )
        case _:
            return entries
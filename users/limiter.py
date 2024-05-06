from django_limits.limiter import Limiter
from django.db.models import Q
from django.contrib.auth.models import User


class UserLimiter(Limiter):
    rules = {
        User: [
            {
                'limit': 70,
                'message': "Only 70 active users allowed",
                'filterset': Q(is_active=True)
            },
            {
                'limit': 5,
                'message': "Only 5 staff members allowed",
                'filterset': Q(is_staff=True)
            }
        ]
    }
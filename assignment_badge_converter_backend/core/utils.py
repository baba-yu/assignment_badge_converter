from django.contrib.auth import get_user_model


def unique_username_from_email(email: str) -> str:
    User = get_user_model()
    base = (email.split("@")[0] or "user")[:150]
    candidate = base
    suffix = 1
    while User.objects.filter(username=candidate).exists():
        tail = str(suffix)
        candidate = f"{base[:150 - len(tail)]}{tail}"
        suffix += 1
    return candidate

from __future__ import annotations
from typing import Dict, Iterable, List, Tuple, Any
from django.conf import settings

SENSITIVE_KEYS = {
    "SECRET_KEY", "DATABASES", "EMAIL_HOST_PASSWORD", "EMAIL_HOST_USER",
    "SENTRY_DSN", "SENTRY_ENVIRONMENT", "AWS_SECRET_ACCESS_KEY", "AWS_ACCESS_KEY_ID",
}

# Что показываем на странице — ключи по группам
WHITELIST: Dict[str, Iterable[str]] = {
    "Core": (
        "DEBUG", "ALLOWED_HOSTS", "TIME_ZONE", "USE_TZ", "LANGUAGE_CODE",
        "INSTALLED_APPS", "MIDDLEWARE",
    ),
    "Static & Media": ("STATIC_URL", "STATIC_ROOT", "MEDIA_URL", "MEDIA_ROOT"),
    "Database": ("DATABASES",),
    "Security": (
        "CSRF_COOKIE_SECURE", "SESSION_COOKIE_SECURE",
        "SECURE_SSL_REDIRECT", "X_FRAME_OPTIONS",
    ),
    "REST": ("REST_FRAMEWORK",),
}

def _mask(value: Any, key: str) -> Any:
    if key in SENSITIVE_KEYS:
        return "********"
    return value

def _db_summary() -> Dict[str, Any]:
    try:
        default = settings.DATABASES["default"]
        return {
            "ENGINE": default.get("ENGINE", ""),
            "NAME": default.get("NAME", ""),
            "HOST": default.get("HOST", ""),
            "PORT": default.get("PORT", ""),
            "USER": default.get("USER", ""),
        }
    except Exception:
        return {}

def settings_context(request):
    groups: List[Tuple[str, List[Tuple[str, Any]]]] = []

    for group, keys in WHITELIST.items():
        rows: List[Tuple[str, Any]] = []
        for key in keys:
            try:
                if key == "DATABASES":
                    value = _db_summary()  # компактнее
                else:
                    value = getattr(settings, key)
            except Exception:
                continue
            rows.append((key, _mask(value, key)))
        groups.append((group, rows))

    # Дополнительно — короткие «бейджи» наверху
    badges = {
        "DEBUG": settings.DEBUG,
        "TIME_ZONE": settings.TIME_ZONE,
        "LANGUAGE_CODE": settings.LANGUAGE_CODE,
        "APPS": len(getattr(settings, "INSTALLED_APPS", [])),
        "MIDDLEWARE": len(getattr(settings, "MIDDLEWARE", [])),
    }

    return {
        "settings": settings,         # оставим для точечного доступа
        "settings_groups": groups,    # [(group, [(key, value), ...]), ...]
        "settings_badges": badges,
    }

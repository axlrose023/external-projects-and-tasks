"""
ASGI config for website project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
import django
from django.conf import settings
from django.core.asgi import get_asgi_application


from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
django.setup()

from userdata.routers import userdata_router


def get_application() -> FastAPI:
    app = FastAPI(debug=settings.DEBUG)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_origin_regex=settings.CORS_ALLOWED_ORIGINS_REGEX,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(userdata_router)
    app.mount("/django" if settings.DEBUG else "/", get_asgi_application())
    app.mount("/media", StaticFiles(directory="media"), name="media")

    if settings.DEBUG:
        app.mount("/static", StaticFiles(directory="allstaticfiles"), name="static")

    add_pagination(app)

    return app


app = get_application()

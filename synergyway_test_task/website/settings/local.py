# region				-----External Imports-----
import os
from dotenv import load_dotenv

# endregion

# region				-----Internal Imports-----
from .django import *
from .project import *
from .third_party import *

# endregion

load_dotenv()

SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-f3b^5-n1zgjz&(6vl=uykrs6kppw1k)xov8)y^**!d0a-zp!l^"
)

DEBUG = True

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1,0.0.0.0").split(
    ","
)

DATABASES = {
    "default": {
        "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
        "HOST": os.environ.get("DATABASE_HOST"),
        "NAME": os.environ.get("DATABASE_NAME"),
        "PORT": os.environ.get("DATABASE_PORT"),
        "USER": os.environ.get("DATABASE_USER"),
        "ENGINE": os.environ.get("ENGINE"),
        "ATOMIC_REQUESTS": True,
        "TEST": {
            "NAME": "tests",
        },
    }
}

CORS_ALLOWED_ORIGINS = os.environ.get(
    "CORS_ALLOWED_ORIGINS",
    "http://127.0.0.1:3000,http://127.0.0.1,http://localhost:3000,http://localhost",
).split(",")

CORS_ALLOWED_ORIGINS_REGEX = os.environ.get(
    "CORS_ALLOWED_ORIGINS_REGEX",
    "http://(127.0.0.1|localhost)(:3000)?",
)

print(">>> START PROJECT WITH LOCAL SETTINGS <<<")

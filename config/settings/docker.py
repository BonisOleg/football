"""Settings for Docker Compose: TLS terminates at nginx, Gunicorn serves HTTP."""

from .production import *  # noqa: F403, F401

SECURE_SSL_REDIRECT = False

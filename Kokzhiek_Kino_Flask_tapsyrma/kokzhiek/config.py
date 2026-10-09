import os


class Config:
    SECRET_KEY = os.environ.get("KOKZHIEK_SECRET_KEY", "kokzhiek-dev-secret-key")
    CSRF_ENABLED = True
    MAX_SEATS = 6
    DISCOUNT_PERCENT = 30
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

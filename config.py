import os
class Config:
    SECRET_KEY = "datasetmanager@2025*"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    # SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "Lax"

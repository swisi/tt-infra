import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'tt-infra-dev-secret')
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('SQLALCHEMY_DATABASE_URI')
        or os.environ.get('DATABASE_URL')
        or 'sqlite:///infra.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    INTERNAL_API_SECRET = os.environ.get('INTERNAL_API_SECRET', 'tt-internal-dev-secret-change-me')
    AUTO_CREATE_DB = os.environ.get('AUTO_CREATE_DB', 'true').lower() == 'true'
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()

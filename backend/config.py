import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "SuperSuperDuperSecretKey")

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///citypulse.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "AnotherSuperDuperSecretKey")
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)

    S3_CONFIG = {
        "endpoint_url": "https://us-003.s3.synologyc2.net",
        "aws_access_key_id": "uspP7MHv7g1jNFePQNzMmVm3EPApqb91",
        "aws_secret_access_key": "TmDOiMhLRQdVtJLm3Rw7G7DosbSh1Kmn",
        "bucket_name": "citypulse",
        "region_name": "us-003",
    }

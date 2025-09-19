import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "SuperSuperDuperSecretKey")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql://wsl:soham%40123@localhost:5432/city_pulse"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "AnotherSuperDuperSecretKey")
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_ACCESS_TOKEN_EXPIRES = 36000

    S3_CONFIG = {
        "endpoint_url": "https://us-003.s3.synologyc2.net",
        "aws_access_key_id": "us2U1G1ii6Rt6tHwSapHstBZLqAlXF91",
        "aws_secret_access_key": "wAPT0oKP3CD1E4SIEit5DvemLqpWbcmF",
        "bucket_name": "citypulse",
        "region_name": "us-east-1",
    }

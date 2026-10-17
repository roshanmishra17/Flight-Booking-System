from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv("ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
)

REDIS_URL = os.getenv("REDIS_URL")

EMAIL_API_KEY = os.getenv("EMAIL_API_KEY")

EMAIL_SENDER = os.getenv("EMAIL_SENDER")

EMAIL_SENDER_NAME= os.getenv("EMAIL_SENDER_NAME")
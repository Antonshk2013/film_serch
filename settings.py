import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-key")
    DEBUG = os.environ.get("DEBUG", "True") == "True"

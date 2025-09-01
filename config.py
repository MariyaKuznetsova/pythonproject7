import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv("database.ini")

CURRENT_FILE = Path(__file__).resolve()
ROOT_DIR = CURRENT_FILE.parent

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PORT = os.getenv("DB_PORT")
DB_HOST = os.getenv("DB_HOST")
DB_PASSWORD = os.getenv("DB_PASSWORD")

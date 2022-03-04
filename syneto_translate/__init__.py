import os

from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv('GOOGLE_PROJECT_ID')
SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

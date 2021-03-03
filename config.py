import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("token")
db_name = os.getenv("DB_NAME")
admin_id = int(os.getenv("ADMIN_ID"))
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
host = "localhost"

I18N_DOMAIN = 'gamebot'
BASE_DIR = Path(__file__).parent
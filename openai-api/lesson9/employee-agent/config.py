'''
One advantage is that we can now change environments without modifying code.

Development
     │
     ▼
localhost Oracle

Production
     │
     ▼
OCI Oracle

'''

import os
from dotenv import load_dotenv

load_dotenv()
api_key=os.getenv('OPENAI_API_KEY')

# ==========================================================
# OpenAI
# ==========================================================
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")

# ==========================================================
# Oracle
# ==========================================================
ORACLE_USER = os.environ["ORACLE_USER"]
ORACLE_PASSWORD = os.environ["ORACLE_PASSWORD"]
ORACLE_DSN = os.environ["ORACLE_DSN"]

# ==========================================================
# REST
# ==========================================================
FRANKFURTER_URL = os.getenv("FRANKFURTER_URL", "https://api.frankfurter.dev/v2")

# ==========================================================
# Application
# ==========================================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

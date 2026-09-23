import os
from dotenv import load_dotenv

load_dotenv()
api_key=os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = "gpt-4.1-mini"
ORACLE_USER = os.environ["ORACLE_USER"]
ORACLE_PASSWORD = os.environ["ORACLE_PASSWORD"]
ORACLE_DSN = os.environ["ORACLE_DSN"]

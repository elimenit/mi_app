# Funcionamiento de python-dotenv
# .env -> MY_PASSWORD = "ALGO"
"""
from dotenv import load_dotenv
import os

load_dotenv()
password = os.getenv("MY_PASSWORD")
print(password)
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILIY_API_KEY = os.getenv("TAVILY_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")
if not TAVILIY_API_KEY:
    raise ValueError("TAVILIY_API_KEY is not set in the environment variables.")
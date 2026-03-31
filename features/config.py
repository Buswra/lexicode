"""Central configuration for the LexiCode application."""
from __future__ import annotations

import os
import sys
from pathlib import Path

FEATURES_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = FEATURES_DIR.parent

try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv(PROJECT_ROOT / '.env')
except Exception:
    pass

RESOURCE_DIR = Path(getattr(sys, '_MEIPASS', FEATURES_DIR))

if getattr(sys, 'frozen', False):
    APP_DIR = Path(os.environ.get('LOCALAPPDATA', str(Path.home()))) / 'LexiCode'
else:
    APP_DIR = PROJECT_ROOT

APP_DIR.mkdir(parents=True, exist_ok=True)

APP_NAME = 'LexiCode'
APP_VERSION = '1.2.0'
DEFAULT_HOST = os.getenv('HOST', '127.0.0.1')
DEFAULT_PORT = int(os.getenv('PORT', os.getenv('LEXICODE_PORT', '5000')))
DEBUG = os.getenv('LEXICODE_DEBUG', '0') == '1'
CLAUDE_MODEL = os.getenv('CLAUDE_MODEL', 'claude-sonnet-4-20250514')
DB_PATH = APP_DIR / 'progress.db'

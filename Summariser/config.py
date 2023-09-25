import os
from pathlib import Path


class Config:
    LOGS = Path.cwd() / 'Text-Summariser' / 'logs'
    STATIC = Path.cwd().parent / 'Text-Summariser' / 'static'
    KEY = os.environ.get('OPENAI_API_KEY', None)

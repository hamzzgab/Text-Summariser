from pathlib import Path
from datetime import datetime


class Config:
    LOGS = Path.cwd().joinpath('./logs')

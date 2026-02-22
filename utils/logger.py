import logging
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
LOGS_DIR = ROOT_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if logger.handlers:
        return logger
    
    fh = logging.FileHandler(LOGS_DIR / f"{name}.log", encoding='utf-8')
    fh.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    
    logger.addHandler(fh)
    return logger

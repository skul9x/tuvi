import logging
import os
import sys

def setup_logger(name="TuVi"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
        logger.addHandler(handler)
        
    return logger, None # Return None for signal/slot compatibility if needed by caller

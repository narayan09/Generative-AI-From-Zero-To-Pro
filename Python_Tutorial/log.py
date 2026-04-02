import logging
from datetime import datetime

logging.basicConfig(
    filename ="test.log",
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.DEBUG          # Minimum log level

)

def check_time():
    curr_time = datetime.now()
    logging.info(f"curr_time is {curr_time}")

check_time()

# /home/test/AI_Projects/Generative-AI-From-Zero-To-Pro/.venv/bin/python3

# /home/test/AI_Projects/Generative-AI-From-Zero-To-Pro/Python_Tutorial

# * * * * * /home/test/AI_Projects/Generative-AI-From-Zero-To-Pro/.venv/bin/python3 /home/test/AI_Projects/Generative-AI-From-Zero-To-Pro/Python_Tutorial/log.py

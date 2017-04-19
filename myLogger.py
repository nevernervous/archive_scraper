import logging
import os
from datetime import datetime

log_folder = 'log'

# create logger
logger = logging.getLogger('Main_Logs')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

fh = logging.FileHandler('{}/{}'.format(log_folder, datetime.now().strftime('%H_%M_%d_%m_%Y.log')))
fh.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - \n %(message)s')

# add formatter to ch
ch.setFormatter(formatter)
fh.setFormatter(formatter)

# add handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

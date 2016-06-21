import logging
import logging.config
import time

def logSetup():
    LOG_PATH = 'log/'
    fileName = LOG_PATH + 'runlog.' + str(int(time.time())) + '.out'
    logging.config.fileConfig('config/logging.conf',defaults={'logfilename': fileName})

def getLogger():
    # create logger
    global logger
    logger = logging.getLogger(__name__)

def debug(message):
    #LEVEL 10
    logger.debug(message)

def info(message):
    #LEVEL 20
    logger.info(message)

def warn(message):
    #LEVEL 30
    logger.warning(message)

def error(message):
    #LEVEL 40
    logger.error(message)

def critical(message):
    #LEVEL 50
    logger.critical(message)

#USAGE
#logSetup()
#getLogger()
#info('testing')
#debug('testing')
#warn('testing')
#error('testing')
#critical('testing')

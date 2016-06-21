import logging

def initLog():
     global logger 
     logger = logging.getLogger(__name__)

def sayhi():
    logger = logging.getLogger('poda')
    logger.critical('inside hi')

sayhi()

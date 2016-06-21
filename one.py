import src/shorturl
import logger_org
import logging
import logger
import two
log=logger.logger()
log.logSetup()
log.setLogger(__name__)
log.info('test')
two.test()

logger_org.logSetup()
log = logging.getLogger('ohh')
log.critical(__name__ + ' test')
two.test()

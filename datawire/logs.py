import logging
from logging.handlers import SMTPHandler
from colorlog import ColoredFormatter

from datawire.core import app

logger = logging.getLogger('datawire')
logger.setLevel(logging.DEBUG)

formatter = ColoredFormatter(
    "%(log_color)s%(levelname)-8s[%(threadName)s]%(reset)s %(white)s%(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red',
    }
)

mail_handler = SMTPHandler(app.config.get('SMTP_SERVER', '127.0.0.1'),
                           app.config.get('SMTP_SENDER', 'info@datawi.re'),
                           app.config.get('SYSADMINS'),
                           'datawi.re Exception')
mail_handler.setLevel(logging.ERROR)

if not app.debug:    
    app.logger.addHandler(mail_handler)
else:
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(formatter)
    logger.addHandler(sh)
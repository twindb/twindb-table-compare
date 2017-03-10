# -*- coding: utf-8 -*-
"""
Module to read pr-table-checksum's result table (percona.checksums)
and show user which records are actually different.
"""
import logging
from logutils.colorize import ColorizingStreamHandler

__author__ = 'Aleksandr Kuzminsky'
__email__ = 'aleks@twindb.com'
__version__ = '1.1.3'

LOG = logging.getLogger(__name__)


def setup_logging(logger, debug=False, color=True):
    """
    Configure logging.

    :param logger: Logger to configure.
    :type logger: Logger
    :param debug: If True - print debug messages
    :param color: If True - print colored messages
    """

    fmt_str = "%(asctime)s: %(levelname)s:" \
              " %(module)s.%(funcName)s():%(lineno)d: %(message)s"

    logger.handlers = []
    if color:
        colored_console_handler = ColorizingStreamHandler()
        colored_console_handler.level_map[logging.INFO] = (None, 'cyan', False)
        colored_console_handler .setFormatter(logging.Formatter(fmt_str))
        logger.addHandler(colored_console_handler)
    else:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(fmt_str))
        logger.addHandler(console_handler)

    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

import logging
import sys

# See:
# https://docs.python.org/3.8/library/logging.html

use_manim_logger = True

if use_manim_logger:
    logger = logging.getLogger("manim")
    pass
else:
    logger = logging.getLogger("presentations")
    # logger.setLevel(logging.DEBUG)
    # fmt = logging.Formatter(logging.BASIC_FORMAT)
    fmt = logging.Formatter("%(levelname)s:%(filename)s:%(lineno)s:\t%(message)s")
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    pass

logger.setLevel(logging.DEBUG)
PRESENTATION_INFO = 17
logging.addLevelName(PRESENTATION_INFO, 'PRESENTATION_INFO')

if __name__ == '__main__':
    """Stream test"""
    if sys.stdout not in {getattr(x, 'stream', None) for x in logger.handlers}:
        logger.addHandler(logging.StreamHandler(sys.stdout))
        pass

    logger.info("Test Log")
    logger.log(17, 'Non-standard test log.')

    pass

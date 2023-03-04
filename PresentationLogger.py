import logging
import sys

# See:
# https://docs.python.org/3.8/library/logging.html

TOPIC_INFO = 17
logging.addLevelName(TOPIC_INFO, 'TOPIC')
PPTX_INFO = 15
logging.addLevelName(PPTX_INFO, 'PPTX_INF')
PPTX_DEBUG = 11
logging.addLevelName(PPTX_DEBUG, 'PPTX_DBG')
use_manim_logger = True

if use_manim_logger:
    # logger = logging.getLogger("manim")
    from manim import logger
    # TODO (2023-03-03 @ 15:02:40): look into console._theme_stack to add colors to custom levels
    #  manim.console._theme_stack or manim.console._thread_locals.theme_stack
    # TODO (2023-03-03 @ 15:02:16): Figure out how to change the width of the level name in the logger
    max_level_name_length = max(map(len, map(logging.getLevelName, range(0, 100))))
    # console._log_render.level_width = max_level_name_length  # doesn't work
    pass
else:
    logger = logging.getLogger("presentations")
    # fmt = logging.Formatter(logging.BASIC_FORMAT)
    fmt = logging.Formatter("%(levelname)s:%(filename)s:%(lineno)s:\t%(message)s")
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    pass
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    """Stream test"""
    if sys.stdout not in {getattr(x, 'stream', None) for x in logger.handlers}:
        logger.addHandler(logging.StreamHandler(sys.stdout))
        pass

    logger.info("Test Log")
    logger.log(17, 'Non-standard test log.')

    pass

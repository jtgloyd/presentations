import logging
import sys
import warnings

# TODO (2023-08-19 @ 13:51:40): properly implement __all__
# __all__ = []

# See:
# https://docs.python.org/3.8/library/logging.html

TOPIC_INFO = 17
logging.addLevelName(TOPIC_INFO, 'TOPIC')
TOPIC_DEBUG = 12
logging.addLevelName(TOPIC_DEBUG, 'TPC_DBG')
TOPIC_WARNING = 29
logging.addLevelName(TOPIC_WARNING, 'TPC_WRN')
PPTX_INFO = 15
logging.addLevelName(PPTX_INFO, 'PPTX_INF')
PPTX_DEBUG = 11
logging.addLevelName(PPTX_DEBUG, 'PPTX_DBG')
PPTX_WARNING = 28
logging.addLevelName(PPTX_WARNING, 'PPTX_WRN')

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
# logger.setLevel(logging.DEBUG)
logger.setLevel(logging.WARNING)

# # Make sure warnings are captured by logger
# logging.captureWarnings(True)
# warnings_logger = logging.getLogger("py.warnings")
# warnings_logger.addHandler(logger.handlers[0])
# # ^ Doesn't work

if __name__ == '__main__':
    """Stream test"""
    if sys.stdout not in {getattr(x, 'stream', None) for x in logger.handlers}:
        logger.addHandler(logging.StreamHandler(sys.stdout))
        pass

    logger.info("Test Log")
    logger.log(17, 'Non-standard test log.')

    pass
if __name__ == '__main__':
    """Warning test"""
    warnings.warn("Test warning", Warning, 2)
    pass

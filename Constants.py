__all__ = [
    'UN_FOCUS',

    'STROKE_TO_SCENE_RATIO',
]

# TODO (2023-05-07 @ 09:44:45): import to __init__ and extend __init__.__all__
# TODO (2023-05-07 @ 09:45:54): if this gets too large, then split into separate files by constant type (e.x. colors,
#  etc.)

# Colors
UN_FOCUS = '#666666'

# Ratios
STROKE_TO_SCENE_RATIO = 0.009
# TODO (2023-05-22 @ 14:45:55): write something to test this constant (or derive it)
#   See SCALE_FACTOR_PER_FONT_POINT in tex_mobject.py

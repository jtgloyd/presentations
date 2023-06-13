from .PresentationTopics import *
from custompackages import declarePersonalPackage

declarePersonalPackage(__file__, __package__ if __package__ else 'presentations')

__all__ = [
    'Topic',
    'Slide',
]

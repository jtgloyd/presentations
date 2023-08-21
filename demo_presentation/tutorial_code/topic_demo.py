from presentations import Topic, Slide
from manim import *

class T01_ControllingFocus(Topic):

    @Slide
    def CircleGeneration(self): ...

    @CircleGeneration.child
    def CircleOffset(self): ...

    @CircleGeneration.child
    def CircleMovement(self): ...

    @CircleGeneration.setup
    def CircleGeneration(self, slide: Slide, on=True, *args, **kwargs): ...

    pass
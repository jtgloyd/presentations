@Slide
def CircleGeneration(self): ...

@CircleGeneration.child
def CircleOffset(self): ...

@CircleGeneration.child
def CircleMovement(self): ...

@CircleGeneration.setup
def Circle(self, slide: Slide, on=True, *args, **kwargs
           ):  # Setup for this slide goes here.
    self.circle_0 = Circle(1, color=YELLOW, fill_opacity=1.0)
    pass
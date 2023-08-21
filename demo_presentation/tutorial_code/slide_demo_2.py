@Slide
def CircleGeneration(self):
    self.play(GrowFromCenter(self.circle_0))

    self.wait(0.2)
    self.endSlide(notes="""\
    If I have an object with high contrast...
    """)
    pass

@CircleGeneration.child
def CircleOffset(self):
    self.play(self.circle_0.animate.move_to((UP + LEFT) * 2))

    self.wait(0.2)
    self.endSlide(notes="""\
    The same thing happens when I have the object move.
    """)
    pass

@CircleGeneration.child
def CircleMovement(self):
    self.play(self.circle_0.animate.shift(DOWN * 4))
    self.play(self.circle_0.animate.shift(RIGHT * 4))
    self.play(self.circle_0.animate.shift(UP * 4))
    self.play(self.circle_0.animate.shift(DOWN * 4))
    self.play(self.circle_0.animate.shift(UP * 4))
    self.play(self.circle_0.animate.shift(LEFT * 4))

    self.wait(0.2)
    self.endSlide(notes="""\
    You can expend effort...
    """)
    # Actions and cleanup that don't depend
    # on items for the next slide goes here
    self.play(FadeOut(self.circle_0))
    pass
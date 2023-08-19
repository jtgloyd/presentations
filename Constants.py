__all__ = [
    'UN_FOCUS',

    'STROKE_TO_SCENE_RATIO',
]

# TODO (2023-05-07 @ 09:44:45): import to __init__ and extend __init__.__all__
# TODO (2023-05-07 @ 09:45:54): if this gets too large, then split into separate files by constant type
#  (e.x. colors, etc.)

# Colors
UN_FOCUS = '#666666'

# Ratios
STROKE_TO_SCENE_RATIO = 0.009
# TODO (2023-05-22 @ 14:45:55): write something to test this constant (or derive it)
#   See SCALE_FACTOR_PER_FONT_POINT in tex_mobject.py

# Instructions
LiveTemplateInstructionsForSlide = r'''
In order to get a live template for pycharm, go 
to File -> Settings -> Editor -> Live Templates 
and add a new template called "slide" with the 
following code:

@Slide
def $NAME$(self):
    # Animations and body go here

    self.wait(0.2)
    self.endSlide(notes="""\
""")
    # Actions and cleanup that don't depend 
    # on items for the next slide go here
    pass

Then change the "Applicable in" context to 
Python: class
'''
LiveTemplateInstructionsForTopic = r'''
In order to get a live template for pycharm, go 
to File -> Settings -> Editor -> Live Templates 
and add a new template called "topic" with the 
following code:

class T$N2$_$CLASS_NAME$(Topic):
    _build_command_ = "manim -qm -p $FILE_NAME$ T$N2$_$CLASS_NAME$"

    # noinspection PyAttributeOutsideInit
    def setup(self):
        # Title (replace if necessary)
        self.title0 = Tex(r"\underline{$NAME$}", font_size=72)
        self.title1 = self.title0.copy()
        self.title1.font_size = 24
        self.title1.move_to(3.8 * UP + 6.9 * LEFT, aligned_edge=UL)

        # Other setup goes below
        $END$
        pass

    @Slide
    def Title(self):
        self.play(Write(self.title0, run_time=2))
        self.wait(0.5)
        self.play(Indicate(self.title0))
        self.play(TransformMatchingTex(self.title0, self.title1))
        self.wait(0.2)
        self.endSlide(notes="""\

""")
        pass

    @Slide
    def $SLIDE1$(self):
        # Animations and body go here

        self.wait(0.2)
        self.endSlide(notes="""\

""")
        # Actions and cleanup that don't depend 
        # on items for the next slide goes here
        pass

    @Slide
    def Cleanup(self):
        self.play(FadeOut(self.title1, ...))
        # Put all persistent components in this ^ FadeOut function 
        #  to clean them all up when the topic is finished.
        self.wait(0.2)
        self.endSlide(autonext=True)
        pass

    pass

Then click "Edit Variables" and give a default 
value of ["00"] to N2, ["TITLE"] to NAME, and 
["SLIDE_NAME"] to SLIDE1. Next, give CLASS_NAME
an expression of [capitalize(camelCase(NAME))]
and FILE_NAME an expression of [fileName()] and
turn on "Skip if defined" for CLASS_NAME and 
FILE_NAME. 
Then change the "Applicable in" context to 
Python: Top-level
'''
# TODO (2023-08-19 @ 12:29:02): update these instructions

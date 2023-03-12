# from manim_pptx import PPTXScene
import itertools
import warnings
import typing
import types
import re
import sys
import os

if __name__ == '__main__':
    __package__ = "presentations"
    pass
from .PresentationLogger import logger, TOPIC_INFO
from .PPTXScene import PPTXScene

# TODO: IMPORTANT: It might be possible to improve the conversion to power point by converting the videos for a single
#  slide into one single video, then putting that video into power point as a single playthrough (or something to that 
#  effect).  Alternatively, it might be better to change the self.wait command to not affect the videos, but instead 
#  either pause playback (preferred if possible) or split the videos and add a pause to the slide via animations.

# TODO: add documentation to Topic object that automatically prints either instructions for operation, OR points to
#  the manim instructions for operation, e.g. manim -qm -p Presentation.py T01_...
#  MAYBE add these instructions as a comment in the live templates.

# URGENT: There is an issue with the identification code for finding notes when the notes string is dynamic, e.g.
#  f"""Notes string {var}..."""

# TODO: try using call to __set_name__ to get owner for Slide class, that way we can reference the owner Topic subclass
#  when raising errors and warnings.

# TODO (2023-02-16 @ 08:37:11): Add documentation to Slide class and improve documentation for Topic

# TODO (2023-02-21 @ 13:29:30): Make custom exceptions (and possibly warnings) instead of using the builtin ones

# TODO (2023-03-01 @ 11:30:33): Update live template instructions

# TODO (2023-03-01 @ 11:30:50): Figure out how to get "All" class to re-use video and image resources from other topics

# TODO (2023-03-01 @ 12:57:04): Figure out how to determine when the powerpoint needs to be restarted?

# TODO (2023-03-04 @ 10:47:11): Figure out how to enforce Topic to inherit from different classes, i.e. to enable use
#  of manim_pptx.PPTXScene or other slide show scene options. AND make it so the classes inherited from must have
#  certain methods implemented, similar to ABC meta classes.


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


class Topic(PPTXScene):
    """All slides should be divided, in order, into methods that implement the @Slide decorator class.
    Each slide must end with a self.endSlide(...) command.
    Each slide must have a unique name, and names should be relevant to the content covered.
    Components for use in the slides should be defined in a 'setup' function OR on a per-slide basis using the
        @<slide>.setup decorator

    This is also extensible to other formats of slide show creation using Manim if/when we want to switch over to
    something that doesn't use power point since we've been having so many issues with it (or, when we get overly
    ambitious and want to make our own version *sigh*)"""

    _wait_override_ = None

    @typing.final
    def construct(self):
        # Need to set up previous topics in case of dependence on positions
        for topic in itertools.takewhile(self.__negated_subclasscheck__, Topic.__subclasses__()):
            logger.log(TOPIC_INFO, f'Running setup for {topic.__name__} from {self}')
            # Run global setup from topic
            topic.setup(self)
            # Get slides from topic
            slides = list(topic.__get_slides__())
            # Run slide setup from topic
            topic.slideSetup(self, slides=slides)
            pass
        logger.log(TOPIC_INFO, f'Constructing {self.__class__.__name__}.')
        slides = list(self.__get_slides__())
        self.slideSetup(slides=slides)
        self.slideConstruct(slides=slides)
        pass

    @typing.final
    def __construct_all__(self):
        logger.log(TOPIC_INFO, f'Called "__construct_all__" from {self}')

        # TODO (2023-02-21 @ 12:29:36): Add documentation for this and with naming a subclass "All"
        if len(self.__class__.__bases__) != 1:
            non_unique_base = SyntaxError(
                f'"__construct_all__" method was called by class without a unique base.\n'
                f'\t\tclass: {self.__class__}\n'
                f'\t\tbases: {self.__class__.__bases__}'
            )
            raise non_unique_base
        parent_class = self.__class__.__bases__[0]
        assert issubclass(parent_class, Topic), f'Classes subclassing Topic with name "All" must subclass Topic.'

        topics = [topic for topic in parent_class.__subclasses__()
                  if not isinstance(self, topic)]  # exclude own class to avoid causing loop
        for topic in topics:
            logger.log(TOPIC_INFO, f'Creating {topic.__name__} from {self}')
            # Run global setup from topic
            topic.setup(self)
            # Get slides from topic
            slides = list(topic.__get_slides__())
            # Run slide setup from topic
            topic.slideSetup(self, slides=slides)
            # Construct each slide for topic
            topic.slideConstruct(self, slides=slides)
            pass
        pass

    def __get_instance_slides__(self):
        warnings.warn("The '__get_instance_slides__' method is deprecated, "
                      "use '__get_slides__' instead", DeprecationWarning, 2)
        # TODO (2023-02-21 @ 13:02:55): remove this
        return filter(Slide.__instancecheck__, map(self.__getattribute__, self.__dir__()))

    @classmethod
    def __get_slides__(cls):
        return filter(Slide.__instancecheck__, cls.__dict__.values())

    def wait(self, *args, **kwargs):
        if self._wait_override_ is not None:
            if "duration" not in kwargs and args:
                args = args[1:]
            kwargs["duration"] = self._wait_override_
        return super(Topic, self).wait(*args, **kwargs)

    def __init_subclass__(cls, **kwargs):
        # print(cls.__dict__)
        super(Topic, cls).__init_subclass__()

        # If subclass is named "All" then it is considered special and it's "construct" method is replaced with the
        # "__construct_all__" method.  Furthermore, it may not have any Slide decorated methods itself, and its "setup"
        # method should be identical to the "Topic.setup" method, since these aren't be used by the "__construct_all__"
        # method.
        if cls.__qualname__ == "All":
            if list(cls.__get_slides__()):
                # TODO (2023-02-21 @ 13:13:08): Move this into the Slide class so the error is raised by that line
                #  instead of the "class All(Topic):" line
                slides_in_All = SyntaxError(
                    f'"Slide" decorated methods are not allowed in the special case of subclasses to "Topic"\n'
                    f'\twith the class name "All".'
                )
                raise slides_in_All
            if cls.setup != Topic.setup:
                setup_in_All = SyntaxError(
                    f'"setup" methods are unreachable, and therefore not allowed, in the special case of\n'
                    f'\tsubclasses to "Topic" with the class name "All".'
                )
                raise setup_in_All
            cls.construct = cls.__construct_all__
            # print(os.path.splitext(os.path.split(sys._getframe(1).f_globals['__file__'])[1])[0])
            # cls.__name__ = os.path.splitext(os.path.split(sys._getframe(1).f_globals['__file__'])[1])[0]

            # noinspection PyUnresolvedReferences,PyProtectedMember
            cls.__presentation_name__ = os.path.splitext(os.path.split(sys._getframe(1).f_globals['__file__'])[1])[0]
            # TODO (2023-03-01 @ 10:50:09): Possibly replace this ^ with a class-property implementation of __name__
            pass
        else:
            cls.__presentation_name__ = cls.__name__
        pass

    def slideConstruct(self, **kwargs):
        slides: typing.List[Slide] = kwargs.get('slides', self.__get_slides__())
        for slide in slides:
            slide.constructProtocol(self)
            pass
        pass

    def slideSetup(self, **kwargs):
        slides: typing.List[Slide] = kwargs.get('slides', self.__get_slides__())
        for slide in slides:
            slide.setupProtocol(self)
            pass
        pass

    @classmethod
    def __negated_subclasscheck__(cls, subclass):
        return not cls.__subclasscheck__(subclass)

    pass


class Slide:
    # TODO: figure out how to make name repetition warn the user
    #  (like what happens with re-defined functions within a class)
    name: str
    constructFunction: types.FunctionType
    setupFunction: typing.Optional[types.FunctionType]
    notes: typing.Optional[str]
    code: types.CodeType

    # TODO: figure out how to enforce functions decorated with @NAME.setup to have signature of (self, owner)
    #  -> I think this is going to be done in the inspections or inspections settings (or possibly with a pyi stub)

    def __init__(self, constructFunction: types.FunctionType, setupFunction: types.FunctionType = None):
        self.constructFunction = constructFunction
        self.__on__ = True
        self.setupFunction = setupFunction
        self.__setup__()
        # TODO: convert the values we get out of the code object (and the code object itself) into properties
        #  with setters so the notes and such can be changed from this object?
        pass

    @property
    def code(self) -> types.CodeType:
        # noinspection PyUnresolvedReferences
        return self.constructFunction.__code__

    @property
    def name(self) -> str:
        return self.constructFunction.__name__

    def __setup__(self):
        # consts = self.code.co_consts
        # # FIXME: this needs to be changed because if multiple values of the input are the same, they won't have separate
        # #  entries in the co_consts tuple, i.e. self.endSlide(autonext=True, shownextnotes=True, notes="notes") will
        # #  result in a co_consts tuple of (...,  True, "notes", ('autonext', 'shownextnotes', 'notes'), ...)
        # noteMapIndices = [(index, value) for index, value in enumerate(consts)
        #                   if isinstance(value, tuple) and 'notes' in value]
        #
        # if len(noteMapIndices) == 1:
        #     noteMapIndex, noteMap = noteMapIndices[0]
        #     self.notes = consts[noteMapIndex - len(noteMap) + noteMap.index('notes')]
        # elif len(noteMapIndices) == 0:
        #     self.notes = None
        # else:
        #     raise IndexError(f"Multiple possible notes were located in the code for slide {self.name}")
        self.__processEndSlide__()
        pass

    def __processEndSlide__(self):
        if 'endSlide' in self.code.co_names:
            i1 = self.code.co_varnames.index('self')
            i2 = self.code.co_names.index('endSlide')
            kwEndSlideStart = f"|{chr(i1)}j{chr(i2)}".encode()  # keyword and positional argument call
            poEndSlideStart = f"|{chr(i1)}".encode() + b"\xa0" + f"{chr(i2)}".encode()  # positional only argument call
            endSlideEnd = b'\x01\x00'

            if (self.code.co_code.count(kwEndSlideStart) + self.code.co_code.count(poEndSlideStart)) > 1:
                raise SyntaxError(f"Multiple calls to 'self.endSlide' were detected within a single Slide definition.\n"
                                  f"Please use a new Slide decorated function for each new slide.\n"
                                  f"\t{self.code.co_code.count(kwEndSlideStart)} keyword argument call(s)\n"
                                  f"\t{self.code.co_code.count(poEndSlideStart)} positional only argument call(s)")

            # TODO: figure out how to share code between these two options
            if kwEndSlideStart in self.code.co_code:
                codeStartIndex = self.code.co_code.index(kwEndSlideStart)
                codeEndIndex = self.code.co_code[codeStartIndex:].index(endSlideEnd) + codeStartIndex
                endSlideCode = self.code.co_code[codeStartIndex + len(kwEndSlideStart):codeEndIndex]
                nInputs = endSlideCode[-1]

                try:
                    # print(self.name)
                    # print(endSlideCode[:endSlideCode.index(b'\x8d')].split(b'd')[1:])
                    valueIndices = list(map(ord, endSlideCode[:endSlideCode.index(b'\x8d')].split(b'd')[1:]))
                except TypeError:
                    note_issue = SyntaxWarning(
                        f"\nSyntaxWarning: Issue with obtaining notes (likely due to use of dynamic notes"
                        f"\nstring, i.e. f'...') for slide decorated function:"
                        f"\n\t{self.name}"
                    )
                    warnings.warn(note_issue)
                    self.notes = NotImplemented
                    return None

                values = [self.code.co_consts[i] for i in valueIndices[:-1]]
                prescribedKeywords = self.code.co_consts[valueIndices[-1]]
                keywords = (Topic.endSlide.__code__.co_varnames[1:nInputs - len(prescribedKeywords) + 1] +
                            prescribedKeywords)
                inputDict = dict(zip(keywords, values))
            elif poEndSlideStart in self.code.co_code:
                codeStartIndex = self.code.co_code.index(poEndSlideStart)
                codeEndIndex = self.code.co_code[codeStartIndex:].index(endSlideEnd) + codeStartIndex
                endSlideCode = self.code.co_code[codeStartIndex + len(poEndSlideStart):codeEndIndex]
                nInputs = endSlideCode[-1]

                if nInputs:
                    valueIndices = list(map(ord, endSlideCode[:endSlideCode.index(b'\xa1')].split(b'd')[1:]))
                    values = [self.code.co_consts[i] for i in valueIndices]
                    inputDict = dict(zip(Topic.endSlide.__code__.co_varnames[1:], values))
                else:
                    inputDict = {}
            else:
                raise ValueError(f"Code for constructing a slide indicated there should be a call to 'self.endSlide',\n"
                                 f"but no valid calls were found when inspecting the function's binary.\n\n"
                                 f"code:\n\t{self.code.co_code}\n"
                                 f"consts:\n\t{self.code.co_consts}\n"
                                 f"names:\n\t{self.code.co_names}\n"
                                 f"varnames:\n\t{self.code.co_varnames}")
            # print(self.name, ':', inputDict)

            if 'notes' in inputDict:
                self.notes = inputDict['notes']
            else:
                self.notes = None
        else:
            # TODO: force use of endSlide OR implement endSlide within __call__
            no_end_slide = SyntaxWarning(
                f"\nSyntaxWarning: No call to 'self.endSlide' within Slide decorated function:"
                f"\n\t{self.name}"
            )
            warnings.warn(no_end_slide)
        pass

    def __call__(self, owner, *args, **kwargs):
        warnings.warn("The '__call__' method is deprecated, "
                      "use 'constructProtocol' instead", DeprecationWarning, 2)
        # TODO (2023-03-04 @ 15:58:34): remove this

        logger.log(TOPIC_INFO, f'Called slide "{self.name}"')
        if self.__on__:
            return self.constructFunction(owner, *args, **kwargs)
        # log slide being off
        logger.log(TOPIC_INFO, f'Slide "{self.name}" skipped because it is turned off.')
        pass

    def off(self, off=True):
        self.__on__ = not off
        pass

    def __coreSetup__(self, owner, *args, **kwargs):
        # TODO (2023-03-11 @ 19:12:15): deprecate "off" and use a __off__ method instead of having repeated lines
        #  in the slide setup descriptor
        if not kwargs.get('on', True):
            self.off()
            pass
        pass

    def setup(self, setupFunction: types.FunctionType):
        """ Descriptor to change the setup function for the slide. """
        self.setupFunction = setupFunction
        return self

    def constructProtocol(self, owner, *args, **kwargs):
        if self.__on__:
            logger.log(TOPIC_INFO, f'Constructing slide "{self.name}".')
            return self.constructFunction(owner, *args, **kwargs)
        else:
            # log slide being off
            logger.log(TOPIC_INFO, f'Construction of slide "{self.name}" skipped because it is turned off.')
        pass

    def setupProtocol(self, owner, *args, **kwargs):
        self.__coreSetup__(owner, *args, **kwargs)
        if self.setupFunction is not None:
            logger.log(TOPIC_INFO, f'Executing slide "{self.name}" setup.')
            return self.setupFunction(owner, self, *args, **kwargs)
        else:
            # log "no setup"
            logger.log(TOPIC_INFO, f'Setup for slide "{self.name}" skipped because it has no setup function.')
        pass

    # def __set_name__(self, owner, name):
    #     print(owner, name)
    #     pass

    pass


if __name__ == '__main__0':
    """Initial Testing of Principle"""


    class Test(PPTXScene):
        def testConstruct(self):
            slides = filter(Slide.__instancecheck__, map(self.__getattribute__, self.__dir__()))
            print(*[(slide.name, slide(self)) for slide in slides], sep='\n')
            pass

        pass


    class subTest(Test):
        @Slide
        def slide1(self):
            self.endSlide()
            pass

        def notASlide(self):
            pass

        @Slide
        def slide3(self):
            self.play(run_time=2)

            self.endSlide()
            pass

        def alsoNotASlide(self):
            pass

        @Slide
        def slide2(self):
            pass

        pass


    pass
pass
if __name__ == '__main__1':
    """Testing/Exploration of Code Objects to Pull Out 'endSlide' Command Usage"""


    #
    # class subTest(Topic):
    #     @Slide
    #     def slide1(self):
    #         pass
    #
    #     @Slide
    #     def slide2(self):
    #         self.play(run_time=2)
    #         pass
    #
    #     @Slide
    #     def slide3(self):
    #         self.endSlide()
    #         pass
    #
    #     @Slide
    #     def slide4(self):
    #         self.play(run_time=2)
    #
    #         self.endSlide()
    #         pass
    #
    #     @Slide
    #     def slide5(self):
    #         self.endSlide(notes="test")
    #         pass
    #
    #     @Slide
    #     def slide6(self):
    #         self.play(run_time=2)
    #
    #         self.endSlide(notes="test")
    #         pass
    #
    #     pass
    #
    #
    # # slideCodes = list(filter(Slide.__instancecheck__, subTest.__dict__.values()))
    # slideCodes = {key: value.code
    #               for key, value in subTest.__dict__.items()
    #               if isinstance(value, Slide)}
    # print(*[f"{name}: {code.co_code}"
    #         for name, code in slideCodes.items()], sep='\n')

    class subTest(Topic):
        @Slide
        def slide0(self):
            pass

        @Slide
        def slide1(self):
            self.endSlide(notes="test")
            pass

        @Slide
        def slide2(self):
            self.play(run_time=2)

            self.endSlide(notes="test")
            pass

        @Slide
        def slide3(self):
            self.play(run_time=2)

            self.wait(loop=False)

            # x = 2  # ; y = 3

            # self.endSlide(
            #     notes="test",
            #     loop=False,
            # )

            # self.endSlide(
            #     False,
            #     False,
            #     'test notes',
            #     False
            # )
            # b'|\x00\xa0\x02d\x03d\x03d\x05d\x03\xa1\x04\x01\x00'  # 4 positional arguments
            # b'|\x00\xa0\x02\xa1\x00\x01\x00'  # 0 positional arguments

            self.endSlide(
                False,
                False,
                shownextnotes=False,
                notes='test notes',
            )

            # y = 3
            # return y + x

        pass


    # slideCodes = list(filter(Slide.__instancecheck__, subTest.__dict__.values()))
    slideCodes = {key: value.code
                  for key, value in subTest.__dict__.items()
                  if isinstance(value, Slide)}
    print(*[f"{name}: {code.co_code}"
            for name, code in slideCodes.items()], sep='\n')
    # slideCodes['slide3'].co_code.split(b'\x00')
    # [chr(x) for x in slideCodes['slide3'].co_code]
    pass

    re.split(b'(?<![A-Za-z])\x00', slideCodes['slide3'].co_code)
    # ^ This line should split the code into its different components

    # It looks like the code doesn't particularly have a way of distinguishing between components, one just follows
    # after the other, what I have done in the previous line is take into account the 'self' is referenced by the code
    # b'|\x00j' since 'self' is located at the zero index of co_varnames
    # Therefore, we should be able to find start of the code for self.endSlide(...) by letting i1 be the index of 'self'
    # in co_varnames and i2 be the index of 'endSlide' in co_names, then the start of the desired code is
    # b'|\x{i1}j\x{i2}d'
    # However, b'|\x{i1}\xa0\x{i2}\xa1\x00\x01\x00' represents self.endSlide()

    # Now, let j1, j2, ..., jk be the indices of the keyword argument values in the co_consts tuple, let j0 be the index
    # of the keyword argument names tuple within the co_consts tuple, and let n be the number of keyword arguments, then
    # it looks like for self.endSlide(...) with named arguments gives us:
    # b'|\x{i1}' + b'j\x{i2}' + b'd\x{j1}'    + b'd\x{j2}'    + ... + b'd\x{jk}'    + b'd\x{j0}'  + b'\x8d\x{n}\x01\x00'
    # ^self        ^endSlide    ^kwarg value 1  ^kwarg value 2        ^kwarg value k  ^kwarg names  ^n kwargs and end

    # i1 = subTest.slide3.code.co_varnames.index('self')
    # i2 = subTest.slide3.code.co_names.index('endSlide')
    # kwEndSlideStart = f"|{chr(i1)}j{chr(i2)}".encode()
    # endSlideEnd = b'\x01\x00'
    # codeStartIndex = subTest.slide3.code.co_code.index(kwEndSlideStart)
    # codeEndIndex = subTest.slide3.code.co_code[codeStartIndex:].index(endSlideEnd) + codeStartIndex
    # endSlideCode = subTest.slide3.code.co_code[codeStartIndex + len(kwEndSlideStart):codeEndIndex]
    pass
pass
if __name__ == '__main__2':
    """Testing of __new__ vs __init__ args and order"""


    class testClass:

        def __new__(cls, *args, **kwargs):
            print("In new")
            print(args)
            print(kwargs)
            self = object.__new__(cls)
            return self

        def __init__(self, *args, **kwargs):
            print("In init")
            print(args)
            print(kwargs)
            pass

        pass


    t = testClass('a', 'b', 3, x=2, y=int)
    pass
pass
if __name__ == '__main__3':
    """Subclass method override test."""


    class TestClass:

        def fun1(self):
            print(f'in fun1 of {self}')
            pass

        def fun2(self):
            print(f'in fun2 of {self}')
            pass

        def __init_subclass__(cls, **kwargs):
            super(TestClass, cls).__init_subclass__(**kwargs)
            cls.fun1 = TestClass.fun2
            pass

        pass


    class TestSubClass(TestClass):
        pass


    a = TestClass()
    b = TestSubClass()

    a.fun1()
    a.fun2()

    b.fun1()
    b.fun2()

    pass
pass
if __name__ == '__main__4':
    """Testing of "all" setup with Topic"""


    class subTest(Topic):
        @Slide
        def slide0(self):
            pass

        @Slide
        def slide1(self):
            self.endSlide(notes="test")
            pass

        @Slide
        def slide2(self):
            self.play(run_time=2)

            self.endSlide(notes="test")
            pass

        pass


    a = subTest()
    assert list(a.__get_slides__()) == list(a.__get_instance_slides__())


    class All(Topic):
        # @Slide
        # def slide01(self):
        #     # Animations and body go here
        #
        #     self.wait(0.2)
        #     self.endSlide(notes="""\
        # """)
        #     # Actions and cleanup that don't depend
        #     # on items for the next slide goes here
        #     pass
        #
        # # noinspection PyAttributeOutsideInit
        # @slide01.setup
        # def slide01(self, slide: Slide, on=True, *args, **kwargs):
        #     # Setup for this slide goes here.
        #
        #     # Use slide.off() to turn off this slide
        #     if not on:
        #         slide.off()
        #         pass
        #     pass
        pass


    pass

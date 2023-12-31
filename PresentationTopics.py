__all__ = [
    "Topic",
    "Slide",
]

# from manim_pptx import PPTXScene
import itertools
import time
import warnings
import typing
import types
import sys
import os

if __name__ == '__main__':
    __package__ = "presentations"
    pass
from .PresentationLogger import logger, TOPIC_INFO, TOPIC_DEBUG, TOPIC_WARNING
from .PPTXScene import PPTXScene

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

# TODONT (2023-03-01 @ 11:30:50): Figure out how to get "All" class to re-use video and image resources from other
#  topics
# TODO (2023-08-19 @ 12:19:10): Re-design how "All" works.  Instead of just making one big presentation, it should
#  make the individual presentations, then combine them all together with sections
#  MAYBE using "All" shouldn't be how this is done

# TODO (2023-03-13 @ 16:29:59): Make other Topics within the same script "inherit" the previous Topic's "end state"
#  (maybe check out "play_internal" for ideas how to do this)

# TODO (2023-06-15 @ 19:23:30): Look into using "play_internal" to prep skipped slides (and earlier topics)
#  https://docs.manim.community/en/stable/reference/manim.scene.scene.Scene.html?highlight=remove#manim.scene.scene.Scene.play_internal

# TODO (2023-03-04 @ 10:47:11): Figure out how to enforce Topic to inherit from different classes, i.e. to enable use
#  of manim_pptx.PPTXScene or other slide show scene options. AND make it so the classes inherited FROM must have
#  certain methods implemented, similar to ABC meta classes.

# TODO (2023-05-07 @ 09:06:32): ADD UNIT TESTS!!!!!

# TODO (2023-05-12 @ 09:59:46): Create a pyi file for all classes and modules in this package

# TODO (2023-05-22 @ 12:32:00): When autonext=True, we should combine the two slides together (if applicable) since
#  teams presentations can't use autonext

# TODO (2023-05-24 @ 09:50:44): Change the creation of the slide show to insert the videos into the content section of
#  a "content only" slide, that way the format/layout of the slides can be changed easily by editing the format/layout
#  of a single master slide
#  UPDATE: this isn't exactly how pptx works, but there should still be a way we can do this

# TODO (2023-06-15 @ 14:03:22): use the following method to clean up slide after Topic ends:
#  https://github.com/Elteoremadebeethoven/AnimationsWithManim/blob/master/English/extra/faqs/faqs.md#remove-all-objects-in-screen
#  e.g.: self.play(FadeOut(*self.mobjects))

# URGENT: integrate "Sections" into the way we distinguish slides (and/or topics)
#   https://docs.manim.community/en/stable/tutorials/output_and_config.html#sections

# TODO (2023-07-20 @ 12:07:24): Go to "image_test.py" file for example of how to get images from a scene


class Topic(PPTXScene):
    """All slides should be divided, in order, into methods that implement the @Slide decorator class.
    Each slide must end with a self.endSlide(...) command.
    Each slide must have a unique name, and names should be relevant to the content covered.
    Components for use in the slides should be defined in a 'setup' function OR on a per-slide basis using the
        @<slide name>.setup decorator

    This is also extensible to other formats of slide show creation using Manim if/when we want to switch over to
    something that doesn't use power point since it can cause a lot of issues.
    The main reason behind using power point and MS teams is that when we present live with teams, it downloads a
    local copy of the presentation, so the presentation doesn't eat up bandwidth, but all of the animations come
    through smooth and in full definition."""

    _wait_override_ = None

    @typing.final
    def construct(self):
        self.__setup_dependencies__()
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

    def __setup_dependencies__(self):
        # Need to set up previous topics in case of dependence on positions
        for topic in itertools.takewhile(self.__negated_subclasscheck__, Topic.__subclasses__()):
            logger.log(TOPIC_INFO, f'Running dependency setup for {topic.__name__} from {self}')
            # Run global setup from topic
            topic.setup(self)
            # Get slides from topic, excluding slides that are marked with "skip_dependence=True"
            #                        (usually because they are too expensive)
            slide_options = {slide: slide.setup_defaults for slide in topic.__get_slides__()}
            # slides = [slide for slide, options in slide_options.items()
            #           if not options.get('skip_dependence', False)]
            slides = []
            for slide, options in slide_options.items():
                if not options.get('skip_dependence', False):
                    slides.append(slide)
                    pass
                else:
                    logger.log(TOPIC_DEBUG, f'Dependency setup for {slide.name} in {topic.__name__} skipped because '
                                            f'it is marked with "skip_dependence=True", this is to skip generating '
                                            f'unnecessary dependencies for slides with long setup times.')
                    pass
                pass
            # Run slide setup from topic
            topic.slideSetup(self, slides=slides)
            pass
        pass

    def __get_instance_slides__(self):
        warnings.warn("The '__get_instance_slides__' method is deprecated, "
                      "use '__get_slides__' instead", DeprecationWarning, 2)
        # TODO (2023-02-21 @ 13:02:55): remove this
        return filter(Slide.__instancecheck__, map(self.__getattribute__, self.__dir__()))

    @classmethod
    def __get_slides__(cls) -> typing.Iterable["Slide"]:
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

    @classmethod
    def build_command(cls):
        # TODO (2023-05-09 @ 09:48:46): this should be a class-property
        # TODO (2023-05-09 @ 09:48:18): use "inspect" module:
        #  https://stackoverflow.com/a/697395
        filename = ...
        return f"manim -qm -p {filename} {cls.__name__}"

    pass


class Slide:
    # TODO: figure out how to make name repetition warn the user
    #  (like what happens with re-defined functions within a class)
    name: str
    constructFunction: types.FunctionType
    setupFunction: typing.Optional[types.FunctionType]
    notes: typing.Optional[str]
    code: types.CodeType
    __parent_slide__: "Slide"

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
        # # FIXME: this needs to be changed because if multiple values of the input are
        # #  the same, they won't have separate entries in the co_consts tuple, i.e.
        # #  self.endSlide(autonext=True, shownextnotes=True, notes="notes") will result in
        # #  a co_consts tuple of (...,  True, "notes", ('autonext', 'shownextnotes', 'notes'), ...)
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
            # TODO (2023-08-19 @ 12:11:28): This might be more trouble than it's worth
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
                # raise ValueError(f"Code for constructing a slide indicated there should be a call to 'self.endSlide',\n"
                #                  f"but no valid calls were found when inspecting the function's binary.\n\n"
                #                  f"code:\n\t{self.code.co_code}\n"
                #                  f"consts:\n\t{self.code.co_consts}\n"
                #                  f"names:\n\t{self.code.co_names}\n"
                #                  f"varnames:\n\t{self.code.co_varnames}")
                warnings.warn("Can't find endSlide error, needs to be fixed.")
                "It seems like this comes from using ValueTrackers or updaters of some sort. OR lambda functions"
                return
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

        setup_defaults = self.setup_defaults
        # update the acquired arguments with any specified from the function call
        setup_defaults.update(kwargs)

        if not setup_defaults.get('on', True):
            self.off()
            pass
        pass

    @property
    def setup_defaults(self) -> dict:
        # Get default keyword argument values from the setupFunction
        #           Reference:  https://docs.python.org/3/library/inspect.html
        setup_defaults = dict()
        if self.setupFunction is not None:
            # number of arguments (not including keyword only arguments, * or ** args)
            #       References: https://stackoverflow.com/a/73602293
            #                   https://python-reference.readthedocs.io/en/latest/docs/code/argcount.html
            arg_count = self.setupFunction.__code__.co_argcount
            # number of default arguments
            #       References: https://stackoverflow.com/a/17534006
            #                   https://peps.python.org/pep-3102/
            default_arg_count = len(self.setupFunction.__defaults__)

            # set the defaults for non-keyword only arguments as obtained from the function properties
            setup_defaults = dict(zip(self.setupFunction.__code__.co_varnames[arg_count - default_arg_count:],
                                      self.setupFunction.__defaults__))

            # update with keyword only arguments (if they exist)
            #       References: https://stackoverflow.com/a/17534006
            #                   https://peps.python.org/pep-3102/
            if self.setupFunction.__kwdefaults__ is not None:
                setup_defaults.update(self.setupFunction.__kwdefaults__)
                pass
            pass
        elif self.is_child:
            setup_defaults.update(self.__parent_slide__.setup_defaults)
            pass
        return setup_defaults

    def setup(self, setupFunction: types.FunctionType) -> "Slide":
        """ Descriptor to change/set the setup function for the slide. """
        assert not self.is_child
        self.setupFunction = setupFunction
        return self

    def child(self, constructFunction: types.FunctionType) -> "Slide":
        """
        Decorator to set a new child slide.

        Define an additional slide which relies of the same setup as this slide,
        which should come after this slide or after other child slides of this
        slide.
        """
        # TODO (2023-06-13 @ 17:44:15): (low priority) make a postfix completion template for this
        child_slide = Slide(constructFunction)
        child_slide.__parent_slide__ = self
        return child_slide

    @property
    def is_child(self):
        return hasattr(self, "__parent_slide__")

    def constructProtocol(self, owner, *args, **kwargs):
        if self.__on__:
            # TODO (2023-03-13 @ 12:52:32): add "from {self.parent}" to this log message
            logger.log(TOPIC_INFO, f'Constructing slide "{self.name}".')
            return self.constructFunction(owner, *args, **kwargs)
        else:
            # log slide being off
            logger.log(TOPIC_INFO, f'Construction of slide "{self.name}" skipped because it is turned off.')
        pass

    def setupProtocol(self, owner, *args, **kwargs):
        t_start = time.perf_counter()
        self.__coreSetup__(owner, *args, **kwargs)
        if self.is_child:
            logger.log(TOPIC_INFO, f'Setup for child slide "{self.name}" inherits from parent slide.')
            result = None
            pass
        elif self.setupFunction is not None:
            logger.log(TOPIC_INFO, f'Executing slide "{self.name}" setup.')
            result = self.setupFunction(owner, self, *args, **kwargs)
            pass
        else:
            # log "no setup"
            logger.log(TOPIC_INFO, f'Setup for slide "{self.name}" skipped because it has no setup function.')
            result = None
            pass
        dt = time.perf_counter() - t_start

        # TODO (2023-03-13 @ 15:06:43): Warn the user if the setup should be marked with "skip_dependence=True" to
        #  save time.  This should also check to see if the setup elements were obtained from hashed components.
        #  (i.e. because creating the latex components takes a while, but then they are saved)
        # TODO (2023-05-12 @ 14:01:41): This should also check if the setup is being run for dependence OR being run
        #  for the setup of the slide being created, because in the latter case, then dependence doesn't really matter
        #  because all aspects of the setup are required and therefore in this case, this warning shouldn't be raised.
        if dt > 1 and not self.setup_defaults.get('skip_dependence', False):
            # TODO (2023-06-18 @ 15:17:16): owner.__presentation_name__ is not correct because it will always be
            #  the Topic doing the setup, not the actual owner of the slide.
            logger.log(TOPIC_WARNING, f'The setup for Slide decorated function {self.name} in '
                                      f'{owner.__presentation_name__} is computationally expensive.  If there are no '
                                      f'dependencies in this setup function for slides in other Topics, then consider '
                                      f'adding "skip_dependence=True" to the setup function\'s arguments.  If there '
                                      f'are dependencies in this setup, then consider adding exclusively the dependent '
                                      f'components to the Topic\'s setup method.')
            pass

        return result

    # def __set_name__(self, owner, name):
    #     print(owner, name)
    #     pass

    pass

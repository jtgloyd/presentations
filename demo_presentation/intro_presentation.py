from presentations import Topic, Slide
from manim import *

UN_FOCUS = '#444444'  # GREY_D
preamble_addition = """
\\usepackage{mathtools}
\\usepackage{amssymb}

\\usepackage{xfp}
\\newcommand{\\tensor}[2]{
    \\ifnum 1<#1
        \\underline{\\tensor{\\fpeval{#1-1} }{#2} }
    \\else
        \\underline{#2}
    \\fi
}

\\newcommand{\\T}[1]{
    #1^{T}
}

\\newcommand{\\bigO}[1]{%
    \\mathcal{O}%
    % O%
    \\left( #1 \\right)
}

\\newcommand{\\sgn}[1]{
    \\mathrm{sgn} \\!\\left( #1 \\right)
}
\\newcommand{\\sgnc}[1]{
    \\mathrm{sgn} \\!\\left< #1 \\right>
}
"""
if preamble_addition not in config["tex_template"].preamble:
    config["tex_template"].add_to_preamble(preamble_addition)
    pass


class T01_Examples(Topic):
    _build_command_ = "manim -qm -p intro_presentation.py T01_Examples"
    _wait_override_ = None

    # noinspection PyAttributeOutsideInit
    def setup(self):  # Setup not attached to specific slides goes below
        pass

    @Slide
    def Intro(self):
        # Animations and body go here
        self.play(self.banner.create())
        self.play(self.banner.expand())

        self.wait(0.2)
        self.endSlide(notes="""\
        This is a quick introduction to using the Manim software package for presentations.
        """)
        # Actions and cleanup that don't depend
        # on items for the next slide goes here
        self.play(Unwrite(self.banner))
        pass

    # noinspection PyAttributeOutsideInit,PyUnusedLocal
    @Intro.setup
    def Intro(self, slide: Slide, on=True, *args, **kwargs):  # Setup for this slide goes here.
        self.banner = ManimBanner()
        pass

    @Slide
    def TensorVisualization(self):
        # Animations and body go here
        self.play(Write(self.problem_statement1))

        self.wait(0.2)
        self.endSlide(notes="""\
        I was originally drawn to the Manim software because it renders\
        mathematics so beautifully.
        """)
        # Actions and cleanup that don't depend
        # on items for the next slide goes here
        self.play(self.problem_statement1.animate.move_to(2 * UP))
        pass

    @TensorVisualization.child
    def TensorVisualizationGeometry(self):
        # Animations and body go here
        angle = -45 * DEGREES
        axis = np.array([-1., 1., 0.])
        run_time = 2.0

        self.play(FadeToColor(self.problem_statement1.get_part_by_tex(r'\tensor{1}{x}'), self.x_obj0.color),
                  FadeIn(self.x_obj0), run_time=run_time)
        self.play(FadeToColor(self.problem_statement1.get_part_by_tex(r'\tensor{3}{K}'), self.K_obj0.color),
                  FadeIn(self.K_obj0),
                  FadeIn(self.xK_dot0), run_time=run_time)
        self.play(FadeToColor(self.problem_statement1.get_part_by_tex(r'\tensor{1}{u}'), self.u_obj0.color),
                  FadeIn(self.u_obj0),
                  FadeIn(self.uK_dot0), run_time=run_time)
        self.play(FadeToColor(self.problem_statement1.get_part_by_tex(r'\tensor{1}{f}'), self.f_obj0.color),
                  FadeIn(self.f_obj0),
                  FadeIn(self.f_equals0), run_time=run_time)

        self.play(self.K_obj0.animate.rotate(angle, axis=axis),
                  self.x_obj0.animate.rotate(angle, axis=axis),
                  self.u_obj0.animate.rotate(angle, axis=axis),
                  self.f_obj0.animate.rotate(angle, axis=axis),
                  run_time=2.0)

        self.wait(0.2)
        self.endSlide(notes="""\
        But the primary benefit for Manim is in visualizations.

        It helps us demonstrate ideas in ways that may be easier\
        for an audience to digest.
        """)
        # Actions and cleanup that don't depend
        # on items for the next slide goes here
        pass

    # noinspection PyAttributeOutsideInit,PyUnusedLocal
    @TensorVisualization.setup
    def TensorVisualization(self, slide: Slide, on=True, skip_dependence=True, *args, **kwargs
                            ):  # Setup for this slide goes here.
        self.problem_statement1 = Tex(
            r"{{\tensor{1}{f} }} = {{\tensor{1}{u} }} \cdot {{\tensor{3}{K} }} \cdot {{\tensor{1}{x} }}",
            tex_environment="equation*"
        )

        self.K_obj0 = Prism([2, 3, 2])
        self.K_obj0.color = BLUE

        self.x_obj0 = Line3D(np.array([0, 0, 0]), np.array([0, 3, 0]))
        self.x_obj0.move_to(2.25 * RIGHT)
        self.x_obj0.color = RED
        self.xK_dot0 = Dot(1.75 * RIGHT)

        self.u_obj0 = Line3D(np.array([0, 0, 0]), np.array([2, 0, 0]))
        self.u_obj0.move_to(3.25 * LEFT)
        self.u_obj0.color = GREEN
        self.uK_dot0 = Dot(1.85 * LEFT)

        self.f_obj0 = Line3D(np.array([0, 0, 0]), np.array([0, 0, 2]))
        self.f_obj0.move_to(5.35 * LEFT)
        self.f_obj0.color = YELLOW
        self.f_equals0 = Tex(r'$=$', font_size=48)
        self.f_equals0.move_to(4.7 * LEFT)

        Group(self.K_obj0, self.x_obj0, self.xK_dot0, self.f_obj0, self.f_equals0, self.u_obj0, self.uK_dot0
              ).move_to(DOWN)
        pass

    @Slide
    def Cleanup(self):
        self.play(FadeOut(*self.mobjects))
        # Put all persistent components in this ^ FadeOut function
        # to clean them all up when the topic is finished.
        self.wait(0.2)
        self.endSlide(autonext=True)
        pass

    pass


class T02_Philosophy(Topic):
    _build_command_ = "manim -qm -p intro_presentation.py T02_Philosophy"
    _wait_override_ = None

    # noinspection PyAttributeOutsideInit
    def setup(self):  # Setup not attached to specific slides goes below
        pass

    @Slide
    def MainDifference(self):
        # Animations and body go here
        self.play(Write(self.presentation_tex_0, lag_ratio=0.5))

        self.wait(0.2)
        self.endSlide(notes="""\
        Now, the main difference between a presentation, which\
        is a live or dynamic version of communication,...
        """)
        # Actions and cleanup that don't depend
        # on items for the next slide goes here
        self.play(self.presentation_tex_0.animate.move_to(LEFT * config.frame_x_radius * 0.5).set_color(UN_FOCUS))
        pass

    @MainDifference.child
    def MainDifferenceOther(self):
        # Animations and body go here
        self.other_tex_0.move_to(RIGHT * config.frame_x_radius * 0.5)
        self.play(Write(self.other_tex_0, lag_ratio=0.5))

        self.wait(0.2)
        self.endSlide(notes="""\
        ... and other forms of communication, like papers and posters, ...
        """)
        # Actions and cleanup that don't depend
        # on items for the next slide goes here
        self.play(self.other_tex_0.animate.set_color(UN_FOCUS))
        pass

    @MainDifference.child
    def MainDifferenceRefocus(self):
        # Animations and body go here
        self.play(self.presentation_tex_0.animate.set_color(WHITE))
        self.play(Indicate(self.presentation_tex_0))

        self.wait(0.2)
        self.endSlide(notes="""\
        ... is that you, the presenter, have the opportunity to\
        control your audience's focus or attention.

        If you aren't making presentations with this aspect in mind\
        then your presentations will be sub-optimal.

        So what does this look like?
        """)
        # Actions and cleanup that don't depend
        # on items for the next slide goes here
        self.play(FadeOut(*self.mobjects))
        pass

    # noinspection PyAttributeOutsideInit,PyUnusedLocal
    @MainDifference.setup
    def MainDifference(self, slide: Slide, on=True, *args, **kwargs):  # Setup for this slide goes here.
        self.presentation_tex_0 = Tex("Presentation")
        self.other_tex_0 = Tex(r"Papers, \\Posters, \\Etc...")
        pass

    @Slide
    def Circle(self):
        # Animations and body go here
        self.play(GrowFromCenter(self.circle_0))

        self.wait(0.2)
        self.endSlide(notes="""\
        If I have an object with high contrast appear on the\
        screen, then your focus immediately goes to it.
        """)
        # Actions and cleanup that don't depend
        # on items for the next slide goes here
        pass

    @Circle.child
    def CircleOffset(self):
        # Animations and body go here
        self.play(self.circle_0.animate.move_to((UP + LEFT) * 2))

        self.wait(0.2)
        self.endSlide(notes="""\
        The same thing happens when I have the object move.
        """)
        # Actions and cleanup that don't depend
        # on items for the next slide goes here
        pass

    @Circle.child
    def CircleMovement(self):
        # Animations and body go here
        self.play(self.circle_0.animate.shift(DOWN * 4))
        self.play(self.circle_0.animate.shift(RIGHT * 4))
        self.play(self.circle_0.animate.shift(UP * 4))
        self.play(self.circle_0.animate.shift(DOWN * 4))
        self.play(self.circle_0.animate.shift(UP * 4))
        self.play(self.circle_0.animate.shift(LEFT * 4))

        self.wait(0.2)
        self.endSlide(notes="""\
        You can expend effort to try and focus elsewhere,\
        but your attention is naturally drawn back to the\
        motion of the circle.
        """)
        # Actions and cleanup that don't depend
        # on items for the next slide goes here
        self.play(FadeOut(self.circle_0))
        pass

    # noinspection PyAttributeOutsideInit,PyUnusedLocal
    @Circle.setup
    def Circle(self, slide: Slide, on=True, *args, **kwargs):  # Setup for this slide goes here.
        self.circle_0 = Circle(0.8, color=YELLOW, fill_opacity=1.0)
        pass

    @Slide
    def TwoGoals(self):
        # Animations and body go here

        self.wait(0.2)
        self.endSlide(notes="""\
        To that end, you should keep two goals in mind when making a presentation.
        """)
        # Actions and cleanup that don't depend
        # on items for the next slide goes here
        pass

    @TwoGoals.child
    def TwoGoalsFirstGoal(self):
        # Animations and body go here
        self.play(Write(self.goal_1, lag_ratio=0.5))

        self.wait(0.2)
        self.endSlide(notes="""\
        First, you should make something your audience WANTS to focus on.

        Of course, this is somewhat limited by the topic of what you're\
        presenting, and an underlying axiom here is that your audience\
        actually wants to pay attention.

        But this is where visualizations and animations can really help.\
        I've found people are extremely eager to engage when the information\
        is presented in a visual manner with interesting motivating examples.
        """)
        # Actions and cleanup that don't depend
        # on items for the next slide goes here
        self.play(FadeToColor(self.goal_1, UN_FOCUS))
        pass

    @TwoGoals.child
    def TwoGoalsSecondGoal(self):
        # Animations and body go here
        self.play(Write(self.goal_2, lag_ratio=0.5))

        self.wait(0.2)
        self.endSlide(notes="""\
        Second, you should make it EASY for your audience to focus.\
        Particularly, make it easy for your audience to focus on the parts\
        you want them to focus on.

        These tools can also help with this goal, however a majority of\
        this task comes down to understanding the design principles\
        behind controlling attention and focus.\
        I will share some very useful resources on this later today,\
        and I'm also eventually going to write up some notes on that subject\
        and I'll include that document with the software on github.

        Now I'll go through a quick introduction to the plugin I've made\
        for Manim presentations.
        """)
        # Actions and cleanup that don't depend
        # on items for the next slide goes here
        pass

    # noinspection PyAttributeOutsideInit,PyUnusedLocal
    @TwoGoals.setup
    def TwoGoals(self, slide: Slide, on=True, *args, **kwargs):  # Setup for this slide goes here.
        highlight_color = YELLOW
        self.goal_1 = Tex("1. Make something your audience wants to focus on",
                          tex_to_color_map={"wants": highlight_color})
        self.goal_2 = Tex("2. Make it easy for your audience to focus",
                          tex_to_color_map={"easy": highlight_color})
        self.goal_2.next_to(self.goal_1, DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 2,
                            aligned_edge=LEFT)

        VGroup(self.goal_1, self.goal_2).center()
        pass

    @Slide
    def Cleanup(self):
        self.play(FadeOut(*self.mobjects))
        # Put all persistent components in this ^ FadeOut function
        # to clean them all up when the topic is finished.
        self.wait(0.2)
        self.endSlide(autonext=True)
        pass

    pass


class T03_Tutorial(Topic):
    _build_command_ = "manim -qm -p intro_presentation.py T03_Tutorial"
    _wait_override_ = None

    # noinspection PyAttributeOutsideInit
    def setup(self):  # Setup not attached to specific slides goes below
        self.time_per_character = 0.02
        border_stroke_width = 1

        self.code_0 = Code(file_name="tutorial_code/slide_demo_0.py", font="Monospace",
                           line_spacing=0.65, insert_line_no=False, style="monokai",
                           language="python")
        self.code_0.background_mobject[0].set(color=BLACK, stroke_color=WHITE, stroke_width=border_stroke_width)
        self.code_0.scale_to_fit_height(config.frame_height * 0.95)

        self.code_1 = Code(file_name="tutorial_code/slide_demo_1.py", font="Monospace",
                           line_spacing=0.65, insert_line_no=False, style="monokai",
                           language="python")
        self.code_1.background_mobject[0].set(color=BLACK, stroke_color=WHITE, stroke_width=border_stroke_width)
        self.code_1.scale_to_fit_height(config.frame_height * 0.95)

        self.code_2 = Code(file_name="tutorial_code/slide_demo_2.py", font="Monospace",
                           line_spacing=0.65, insert_line_no=False, style="monokai",
                           language="python")
        self.code_2.background_mobject[0].set(color=BLACK, stroke_color=WHITE, stroke_width=border_stroke_width)
        self.code_2.scale_to_fit_height(config.frame_height * 0.95)

        self.code_3 = Code(file_name="tutorial_code/slide_demo_3.py", font="Monospace",
                           line_spacing=0.65, insert_line_no=False, style="monokai",
                           language="python")
        self.code_3.background_mobject[0].set(color=BLACK, stroke_color=WHITE, stroke_width=border_stroke_width)
        width = self.code_3.scale_to_fit_height(config.frame_height * 0.95).width
        self.code_3.scale_to_fit_width(min(config.frame_width * 0.95, width))

        self.code_4 = Code(file_name="tutorial_code/topic_demo.py", font="Monospace",
                           line_spacing=0.65, insert_line_no=False, style="monokai",
                           language="python")
        self.code_4.background_mobject[0].set(color=BLACK, stroke_color=WHITE, stroke_width=border_stroke_width)
        width = self.code_4.scale_to_fit_height(config.frame_height * 0.95).width
        self.code_4.scale_to_fit_width(min(config.frame_width * 0.95, width))
        pass

    @Slide
    def DecorationSlideDemo(self):
        # Animations and body go here
        # self.play(Create(self.code_0))
        self.play(FadeIn(self.code_0.background_mobject))

        # run_time = sum(map(len, self.code_0[2][:1])) * self.time_per_character
        # self.play(Create(self.code_0[2][:1], run_time=run_time))

        code_lines = self.code_0[2][:1]
        run_time = sum(map(len, code_lines)) * self.time_per_character
        self.play(Create(code_lines, run_time=run_time * 2))

        self.wait(0.2)
        self.endSlide(notes="""\
        Each slide uses the "Slide" decorator...
        """)
        # Actions and cleanup that don't depend
        # on items for the next slide goes here
        pass

    @DecorationSlideDemo.child
    def DecorationSlideDemoFunction(self):
        # Animations and body go here
        # run_time = sum(map(len, self.code_0[2][1:3])) * self.time_per_character
        # self.play(Create(self.code_0[2][1:3], run_time=run_time))
        code_lines = self.code_0[2][1:3]
        run_time = sum(map(len, code_lines)) * self.time_per_character
        self.play(Create(code_lines, run_time=run_time))

        self.wait(0.2)
        self.endSlide(notes="""\
        ... decorating a method which contains the animations\
        and visualizations for that slide.
        """)
        # Actions and cleanup that don't depend
        # on items for the next slide goes here
        pass

    @DecorationSlideDemo.child
    def DecorationSlideDemoBody(self):
        # Animations and body go here

        # TODO (2023-08-20 @ 10:14:08): Add animations demonstrating each part

        code_lines = self.code_0[2][3:5]
        run_time = sum(map(len, code_lines)) * self.time_per_character
        self.play(Create(code_lines, run_time=run_time))

        code_lines = self.code_0[2][5:7]
        run_time = sum(map(len, code_lines)) * self.time_per_character
        self.play(Create(code_lines, run_time=run_time))

        code_lines = self.code_0[2][7:14]
        run_time = sum(map(len, code_lines)) * self.time_per_character
        self.play(Create(code_lines, run_time=run_time * 0.5))

        self.wait(0.2)
        self.endSlide(notes="""\
        The various animations are made using components from Manim,\
        which has a significant amount of documentation online, but\
        it's still very much under development.

        These are the commands used to generate the yellow circle\
        animations you saw earlier.
        """)
        # Actions and cleanup that don't depend
        # on items for the next slide goes here
        pass

    @DecorationSlideDemo.child
    def DecorationSlideDemoEnd(self):
        # Animations and body go here
        code_lines = self.code_0[2][14:18]
        run_time = sum(map(len, code_lines)) * self.time_per_character
        self.play(Create(code_lines, run_time=run_time))

        self.wait(0.2)
        self.endSlide(notes="""\
        We then mark the end of a slide with the "endSlide" method,\
        where we can also include notes that will be directly inserted\
        into the power point slides.\
        There are also some other options that are still under development.

        We also add a wait command before the endSlide to make sure that\
        all the animations finish up, although this may not be necessary in\
        future versions.
        """)
        # Actions and cleanup that don't depend
        # on items for the next slide goes here
        pass

    @DecorationSlideDemo.child
    def DecorationSlideDemoCleanup(self):
        # Animations and body go here
        code_lines = self.code_0[2][18:]
        run_time = sum(map(len, code_lines)) * self.time_per_character
        self.play(Create(code_lines, run_time=run_time))

        self.wait(0.2)
        self.endSlide(notes="""\
        After the endSlide method is called, we can run any clean-up\
        or other animations or commands, which won't be run until we\
        advance to the next slide.
        """)
        # Actions and cleanup that don't depend
        # on items for the next slide goes here
        pass

    # noinspection PyAttributeOutsideInit,PyUnusedLocal
    @DecorationSlideDemo.setup
    def DecorationSlideDemo(self, slide: Slide, on=True, *args, **kwargs):  # Setup for this slide goes here.
        pass

    @Slide
    def SplitSlideDemo(self):
        # Animations and body go here
        # Zoom out and scale
        self.play(self.code_0.animate.scale_to_fit_width(self.code_1.width).move_to(self.code_1))
        self.play(ReplacementTransform(self.code_0.background_mobject, self.code_1.background_mobject))

        code_0_strings = self.code_0.code_string.split('\n')
        code_1_strings = {i: code_line for i, code_line in enumerate(self.code_1.code_string.split('\n'))}
        fade_out_list = []
        transform_source_target_map = []
        skip_create_list = []
        for i, code_line in enumerate(code_0_strings):
            if code_line in code_1_strings.values():
                j = next((index for index, line in code_1_strings.items()
                          if code_line == line))
                transform_source_target_map.append((self.code_0[2][i], self.code_1[2][j]))
                skip_create_list.append(j)
                code_1_strings.pop(j)
            else:
                fade_out_list.append(self.code_0[2][i])
                pass
            pass

        self.play(FadeOut(*fade_out_list, run_time=0.75), AnimationGroup(
            *[ReplacementTransform(source, target)
              for source, target in transform_source_target_map],
            lag_ratio=0.01,
            run_time=3.0,
        ))

        for j, code_line in enumerate(self.code_1[2]):
            if j not in skip_create_list:
                self.play(Create(code_line, run_time=self.time_per_character * len(code_line)))
                pass
            pass

        self.wait(0.2)
        self.endSlide(notes="""\
        Now, what tends to be best practice is to spread out the components\
        over several slides, which makes it easier to match story beats\
        with the corresponding animations.
        """)
        # Actions and cleanup that don't depend
        # on items for the next slide goes here
        pass

    # noinspection PyAttributeOutsideInit,PyUnusedLocal
    @SplitSlideDemo.setup
    def SplitSlideDemo(self, slide: Slide, on=True, *args, **kwargs):  # Setup for this slide goes here.
        pass

    @Slide
    def ChildSlideDemo(self):
        # Animations and body go here
        self.wait(3.0)
        self.play(*[ReplacementTransform(source, target)
                    for source, target in zip(self.code_1[2], self.code_2[2])])
        self.remove(*self.mobjects)
        self.add(self.code_2)

        self.wait(0.2)
        self.endSlide(notes="""\
        Since these slides are all closely related, we can indicate that\
        fact by using the child-slide decorator method.\
        So here, CircleOffset and CircleMovement are children of the 
        CircleGeneration slide.

        Now how do we generate objects for our slides?\
        Well, we can do so within the slide decorated function itself, but ...
        """)
        # Actions and cleanup that don't depend
        # on items for the next slide goes here
        pass

    # noinspection PyAttributeOutsideInit,PyUnusedLocal
    @ChildSlideDemo.setup
    def ChildSlideDemo(self, slide: Slide, on=True, *args, **kwargs):  # Setup for this slide goes here.
        pass

    @Slide
    def SetupSlideDemo(self):
        # Animations and body go here

        # self.code_3.scale_to_fit_width(self.code_2.width)
        # self.code_3.move_to(self.code_2, UP)

        # self.play(TransformMatchingShapes(
        #     self.code_2[2], self.code_3[2][:9], fade_transform_mismatches=True,
        # ))
        # self.play(FadeTransform(
        #     self.code_2[2], self.code_3[2][:9],
        # ), ReplacementTransform(self.code_2.background_mobject, self.code_3.background_mobject))

        index_map = [(0, 0), (1, 1), (10, 3), (11, 4), (20, 6), (21, 7)]
        # transform_map = [
        #     (self.code_2[2][source_index], self.code_3[2][target_index])
        #     for source_index, target_index in index_map
        # ]
        source_indices, target_indices = map(set, zip(*index_map))
        fade_list = [code_line for i, code_line in enumerate(self.code_2[2])
                     if i not in source_indices]

        # self.play(FadeOut(*fade_list))
        # # self.play(ReplacementTransform(self.code_2.background_mobject, self.code_3.background_mobject),
        # #           *[TransformMatchingShapes(source, target, fade_transform_mismatches=False)
        # #             for source, target in transform_map],)
        # self.play(ReplacementTransform(self.code_2.background_mobject, self.code_3.background_mobject),
        #           *[ReplacementTransform(s, t)
        #             for source, target in transform_map
        #             for s, t in zip(source, target)], )
        # self.play(FadeIn(*[target[len(source):]
        #                    for source, target in transform_map]), run_time=0.75)
        ...

        # Create copies of the ellipses functions and then transform in-place,
        #  as the FadeOut is happening, then change position to match code_3
        in_place_transform_map = [
            (self.code_2[2][source_index],
             self.code_3[2][target_index].copy().scale_to_fit_height(self.code_2[2][source_index].height).move_to(
                 self.code_2[2][source_index], LEFT),
             self.code_3[2][target_index])
            for source_index, target_index in index_map
        ]

        self.play(FadeOut(*fade_list),
                  *[TransformMatchingShapes(
                      source, target, key_map=dict(zip(map(TransformMatchingShapes.get_mobject_key, source),
                                                       map(TransformMatchingShapes.get_mobject_key, target))))
                      for source, target, _ in in_place_transform_map]
                  )
        self.play(ReplacementTransform(self.code_2.background_mobject, self.code_3.background_mobject),
                  *[ReplacementTransform(source, target)
                    for _, source, target in in_place_transform_map], )

        code_lines = self.code_3[2][9:]
        run_time = sum(map(len, code_lines)) * self.time_per_character
        self.play(Create(code_lines, run_time=run_time))

        self.wait(0.2)
        self.endSlide(notes="""\
        ... a better way is to do so using the slide setup decorator.

        Here we can instantiate Manim objects or custom objects in a\
        way that's linked to the slide where they are used.\
        There are also key-word arguments, whose defaults let us control\
        the behavior of the slide.\
        For example, you can see we can turn on or off a slide using a\
        key-word argument.

        Now all three slides you see have the same setup function,\
        which is the advantage of using the child slide decorator.\
        If we turn off that slide, then all the child slides are turned\
        off as well.
        """)
        # Actions and cleanup that don't depend
        # on items for the next slide goes here
        self.play(FadeOut(*self.mobjects))
        pass

    # noinspection PyAttributeOutsideInit,PyUnusedLocal
    @SetupSlideDemo.setup
    def SetupSlideDemo(self, slide: Slide, on=True, *args, **kwargs):  # Setup for this slide goes here.
        pass

    @Slide
    def TopicDemo(self):
        # Animations and body go here
        self.play(FadeIn(self.code_4.background_mobject))

        code_lines = self.code_4[2]
        run_time = sum(map(len, code_lines)) * self.time_per_character
        self.play(Create(code_lines, run_time=run_time))

        self.wait(0.2)
        self.endSlide(notes="""\
        Now, we use the slide decorated methods within a sub-class of\
        the Topic class.\
        The Topic class takes care of pretty much everything we need\
        to generate a presentation out of the animations, objects, and\
        other components included in the slide decorated methods.

        There is currently a way of combining Topics into one presentation,\
        but it's bad and I'm working on a much better solution.\
        My current workflow is just to generate the Topics as individual\
        presentations, then combine them manually in power point using the\
        "re-use" slides feature.
        """)
        # Actions and cleanup that don't depend
        # on items for the next slide goes here
        pass

    # noinspection PyAttributeOutsideInit,PyUnusedLocal
    @TopicDemo.setup
    def TopicDemo(self, slide: Slide, on=True, *args, **kwargs):  # Setup for this slide goes here.
        pass

    @Slide
    def Cleanup(self):
        self.play(FadeOut(*self.mobjects))
        # Put all persistent components in this ^ FadeOut function
        # to clean them all up when the topic is finished.
        self.wait(0.2)
        self.endSlide(autonext=True)
        pass

    pass


class All(Topic):
    pass


if __name__ == '__main__':
    """
    This compiles and renders the presentations.
    
    Note, the presentations can also be compiled and rendered using the Manim
    command line interface. 
    """

    with tempconfig({"quality": "medium_quality", "preview": True}):
        topic_01 = T01_Examples()
        topic_01.render()

        topic_02 = T02_Philosophy()
        topic_02.render()

        topic_03 = T03_Tutorial()
        topic_03.render()
        pass

    pass

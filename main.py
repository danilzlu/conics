from manim import *

a = 3
b = 2
e = np.sqrt(1 - b**2/a**2)
c = np.sqrt(a**2 - b**2)


class OpeningManim(Scene):
    def construct(self):
        title = Tex(r"This is some \LaTeX")
        basel = MathTex(r"\sum_{n=1}^\infty \frac{1}{n^2} = \frac{\pi^2}{6}")
        VGroup(title, basel).arrange(DOWN)
        self.play(
            Write(title),
            FadeIn(basel, shift=DOWN),
        )
        self.wait()

        transform_title = Tex("That was a transform")
        transform_title.to_corner(UP + LEFT)
        self.play(
            Transform(title, transform_title),
            LaggedStart(*[FadeOut(obj, shift=DOWN) for obj in basel]),
        )
        self.wait()

        grid = NumberPlane()
        grid_title = Tex("This is a grid", font_size=72)
        grid_title.move_to(transform_title)

        self.add(grid, grid_title)  # Make sure title is on top of grid
        self.play(
            FadeOut(title),
            FadeIn(grid_title, shift=UP),
            Create(grid, run_time=3, lag_ratio=0.1),
        )
        self.wait()

        grid_transform_title = Tex(
            r"That was a non-linear function \\ applied to the grid"
        )
        grid_transform_title.move_to(grid_title, UL)
        grid.prepare_for_nonlinear_transform()
        self.play(
            grid.animate.apply_function(
                lambda p: p
                          + np.array(
                    [
                        np.sin(p[1]),
                        np.sin(p[0]),
                        0,
                    ]
                )
            ),
            run_time=3,
        )
        self.wait()
        self.play(Transform(grid_title, grid_transform_title))
        self.wait()


class CircleIntro(Scene):
    def construct(self):
        grid = NumberPlane(x_range=(-10, 10, 1), y_range=(-10, 10, 1),
                           x_length=20, y_length=20)
        circle = Circle(radius=3)
        circleGroup = VGroup(grid, circle)

        self.play(
            circleGroup.animate.apply_function(
                lambda p: np.array([p[0], p[1]/2, p[2]]) ), run_time=3)
        self.wait()


class EllipsDefi(Scene):
    def construct(self):
        def ellips_get_dot(t):
            return np.array([
                a * np.sin(t),
                b * np.cos(t),
                0
            ])

        ellipsT = ValueTracker(0)

        F1 = Dot((-c, 0, 0))
        F2 = Dot(( c, 0, 0))

        radius11 = Line((-a, 3, 0), (0, 3, 0), buff=0)
        radius21 = Line((0, 3, 0), (a, 3, 0), buff=0)

        ellipsDot = Dot(ellips_get_dot(ellipsT.get_value()), color=RED)
        ellipsDot.add_updater(
            lambda mob: mob.become(
                Dot(ellips_get_dot(ellipsT.get_value()), color=RED)
            )
        )

        radius1 = Line(F1.get_center(), ellipsDot.get_center())
        radius2 = Line(ellipsDot.get_center(), F2.get_center())

        radius1.add_updater(
            lambda mob: mob.become(
                Line(F1.get_center(), ellips_get_dot(ellipsT.get_value()))
            )
        )
        radius2.add_updater(
            lambda mob: mob.become(
                Line(ellips_get_dot(ellipsT.get_value()), F2.get_center())
            )
        )


        self.play(Create(VGroup(F1, F2)))
        self.play(Create(radius11))
        self.play(Create(radius21))
        self.play(Transform(radius11, radius1),
                  Transform(radius21, radius2))
        self.add(radius1, radius2)
        self.wait()
        self.play(Create(ellipsDot), Uncreate(radius11), Uncreate(radius21))
        self.wait()
        self.add(TracedPath(ellipsDot.get_center, stroke_color=ellipsDot.get_color()))
        self.play(ellipsT.animate.set_value(2 * PI), run_time=6)
        self.wait()



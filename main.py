from manim import *
import os


a = 3
b = 2
e = np.sqrt(1 - b**2/a**2)
c = np.sqrt(a**2 - b**2)
radiusColor = ORANGE
ellipsDotColor = RED


def norm(v):
    return v / np.linalg.norm(v)


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


def ellips_get_dot(t):
    return np.array([
        a * np.sin(t),
        b * np.cos(t),
        0
    ])


class EllipsDefi(Scene):
    def construct(self):


        ellipsT = ValueTracker(0)
        ellips = ParametricFunction(ellips_get_dot, t_range=np.array([0, TAU]), fill_opacity=0).set_color(ellipsDotColor)

        ellipsDefiSumFormula = MathTex("|F_1", "O", "| + |F_2", "O", "| = ", "2a")
        ellipsDefiSumFormula[1].set_color(ellipsDotColor)
        ellipsDefiSumFormula[3].set_color(ellipsDotColor)
        ellipsDefiSumFormula[5].set_color(radiusColor)
        cornerDefiSumFormula = ellipsDefiSumFormula.copy().to_corner(UP + LEFT)

        ellipsDot = Dot(ellips_get_dot(ellipsT.get_value()), color=RED).set_color(ellipsDotColor)
        ellipsDot.add_updater(
            lambda mob: mob.become(
                Dot(ellips_get_dot(ellipsT.get_value()), color=RED).set_color(ellipsDotColor)
            )
        )
        ellipsDotName = MathTex("O").next_to(ellipsDot.get_center()).set_color(ellipsDotColor)
        ellipsDotName.add_updater(
            lambda mob: mob.become(
                MathTex("O").next_to(ellips_get_dot(ellipsT.get_value()),
                                     norm(ellips_get_dot(ellipsT.get_value()))).set_color(ellipsDotColor)
            )
        )

        F1 = Dot((-c, 0, 0))
        F2 = Dot(( c, 0, 0))
        f1Name = MathTex("F_1").next_to(F1.get_center(), RIGHT/2)
        f2Name = MathTex("F_2").next_to(F2.get_center(), RIGHT/2)

        Hr = 2.5
        radius11 = Line((-a, Hr, 0), (0, Hr, 0), buff=0).set_color(radiusColor)
        radius21 = Line((0, Hr, 0), (a, Hr, 0), buff=0).set_color(radiusColor)

        radius1 = Line(F1.get_center(), ellipsDot.get_center()).set_color(radiusColor)
        radius2 = Line(ellipsDot.get_center(), F2.get_center()).set_color(radiusColor)
        radius1.add_updater(
            lambda mob: mob.become(
                Line(F1.get_center(), ellips_get_dot(ellipsT.get_value())).set_color(radiusColor)
            )
        )
        radius2.add_updater(
            lambda mob: mob.become(
                Line(ellips_get_dot(ellipsT.get_value()), F2.get_center()).set_color(radiusColor)
            )
        )

        radiusName = MathTex("2a").move_to(radius21.get_center()/2 + radius11.get_center()/2).set_color(radiusColor)
        radiusName.add_updater(
            lambda mob: mob.become(
                MathTex("2a").move_to((radius1.get_center() / 2 + radius2.get_center() / 2)).set_color(radiusColor)
            )
        )

        self.play(Write(ellipsDefiSumFormula))
        self.play(Transform(ellipsDefiSumFormula, cornerDefiSumFormula))
        self.play(Create(VGroup(F1, F2)), Write(f1Name), Write(f2Name))
        self.play(Create(radius11))
        self.play(Create(radius21))
        self.play(Write(radiusName))
        self.play(Transform(radius11, radius1),
                  Transform(radius21, radius2),
                  Create(ellipsDot))
        self.add_foreground_mobjects(ellipsDot)
        self.play(Write(ellipsDotName))
        self.add(radius1, radius2)
        self.remove(radius21, radius11)
        self.play(Uncreate(radius11), Uncreate(radius21))
        self.wait()
        self.add(TracedPath(ellipsDot.get_center, stroke_color=ellipsDot.get_color()))
        self.play(ellipsT.animate.set_value(2 * PI), run_time=8)
        self.wait()
        self.add(ellips)
        self.play(FadeOut(ellipsDefiSumFormula))
        self.play(FadeOut(ellipsDotName), FadeOut(f1Name), FadeOut(f2Name), FadeOut(ellipsDot),
                  FadeOut(F1), FadeOut(F2), FadeOut(radius1), FadeOut(radius2), FadeOut(radiusName))
        self.wait()


class EllipsFormula(Scene):
    def construct(self):
        ellips = ParametricFunction(ellips_get_dot, t_range=np.array([0, TAU]), fill_opacity=0).set_color(
            ellipsDotColor)

        grid = NumberPlane()
        grid = NumberPlane(x_range = (-4, 4, 1),
                            y_range = (-3, 3, 1))
        f1 = Dot((-c, 0, 0)).shift(3.5*LEFT)
        f2 = Dot((c, 0, 0)).shift(3.5*LEFT)
        f1Name = MathTex("F_1").next_to(f1, DOWN)
        f2Name = MathTex("F_2").next_to(f2, DOWN)
        f1Coords = MathTex("(-c, 0)").next_to(f1, DOWN + RIGHT/2)
        f2Coords = MathTex("( c, 0)").next_to(f2, DOWN)

        t0 = 2/3
        oDot = Dot(ellips_get_dot(t0)).set_color(ellipsDotColor).shift(3.5*LEFT)
        radius1 = Line(f1.get_center(), oDot.get_center()).set_color(radiusColor)
        radius2 = Line(oDot.get_center(), f2.get_center()).set_color(radiusColor)
        radius1Name = MathTex("r_1").next_to(radius1, LEFT).set_color(radiusColor).shift(RIGHT/2)
        radius2Name = MathTex("r_2").next_to(radius2, LEFT).set_color(radiusColor)


        ellipsGroup = VGroup(ellips, grid)

        ellipsGroup.generate_target()
        ellipsGroup.target.shift(3.5*LEFT)

        formula01 = MathTex("|F_1O|", " + ", "|F_2O|", " = 2a").to_corner(UP + RIGHT)
        formula02 = MathTex("r_1", " + ", "r_2", " = 2a", "\\ \\Big|\\ r_1 - r_2").to_corner(UP + RIGHT)
        formula03 = MathTex("(r_1 + r_2)(r_1 - r_2)", " = ", "2a", "(r_1 - r_2)").next_to(formula02, DOWN).shift(LEFT)
        formula04 = MathTex("r_1^2 - r_2^2", " = ", "2a", "(r_1 - r_2)").next_to(formula03, DOWN)



        self.add_foreground_mobjects(ellips)
        self.add(grid)
        #self.play(ReplacementTransform(grid, grid2))
        self.play(MoveToTarget(ellipsGroup))
        self.play(Write(formula01))
        self.play(ReplacementTransform(formula01, formula02[:4]))
        self.play(Write(formula02[4:]))
        self.play(
            TransformFromCopy(VGroup(formula02[:2], formula02[-1]), formula03[0]),
            TransformFromCopy(formula02[3], formula03[1:-1]),
            TransformFromCopy(formula02[-1], formula03[-1]),
            run_time = 4
        )
        self.play(
            TransformFromCopy(formula03, formula04),
            run_time=2
        )
        self.play(Create(f1), Create(f2), Write(f1Name), Write(f2Name))
        self.play(Transform(f1Name, f1Coords), Transform(f2Name, f2Coords))
        self.play(Create(radius1), Create(radius2), Create(oDot), Create(radius1Name), Create(radius2Name))
        self.wait()


if __name__ == '__main__':
    os.system("python -m manim main.py -ql  -p")
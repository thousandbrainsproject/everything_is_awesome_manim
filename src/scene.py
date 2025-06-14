# Copyright 2025 Thousand Brains Project
#
# Copyright may exist in Contributors' modifications
# and/or contributions to the work.
#
# Use of this source code is governed by the MIT
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
"""Scene explaining the everything_is_awesome project setup."""

from manim import (
    BLUE,
    DEGREES,
    GRAY,
    ORIGIN,
    OUT,
    PI,
    RIGHT,
    UP,
    UR,
    WHITE,
    Arrow,
    ArrowTriangleFilledTip,
    Axes,
    Circle,
    Create,
    Cylinder,
    Dot,
    Dot3D,
    DrawBorderThenFill,
    FadeIn,
    FadeOut,
    GrowArrow,
    Line,
    MoveAlongPath,
    Rotate,
    Scene,
    Tex,
    Text,
    ThreeDAxes,
    ThreeDScene,
    VGroup,
    Write,
    config,
    linear,
    np,
)


class Robot(ThreeDScene):  # type: ignore[misc]  # noqa: D101
    def construct(self) -> None:  # noqa: D102, PLR0915
        translate_up = Text("TRANSLATE_UP", font_size=24)
        translate_up.to_corner(UR)
        self.add_fixed_in_frame_mobjects(translate_up)
        self.remove(translate_up)
        translate_down = Text("TRANSLATE_DOWN", font_size=24)
        translate_down.to_corner(UR)
        self.add_fixed_in_frame_mobjects(translate_down)
        self.remove(translate_down)
        orbit_left = Text("ORBIT_LEFT", font_size=24)
        orbit_left.to_corner(UR)
        self.add_fixed_in_frame_mobjects(orbit_left)
        self.remove(orbit_left)
        orbit_right = Text("ORBIT_RIGHT", font_size=24)
        orbit_right.to_corner(UR)
        self.add_fixed_in_frame_mobjects(orbit_right)
        self.remove(orbit_right)

        self.set_camera_orientation(
            phi=147 * DEGREES, theta=147 * DEGREES, gamma=-60 * DEGREES, zoom=0.9
        )
        axes = ThreeDAxes(
            x_range=[-1, 1, 0.25],
            y_range=[-1, 1, 0.25],
            z_range=[-1, 1, 0.25],
            x_length=config.frame_height * 0.9,
            y_length=config.frame_height * 0.9,
            z_length=config.frame_height * 0.9,
            x_axis_config={
                "tick_size": 0.05,
                "tip_shape": ArrowTriangleFilledTip,
                "tip_height": 0.1,
                "tip_width": 0.1,
            },
            y_axis_config={
                "tick_size": 0.05,
                "tip_shape": ArrowTriangleFilledTip,
                "tip_height": 0.1,
                "tip_width": 0.1,
            },
            z_axis_config={
                "tick_size": 0.05,
                "tip_shape": ArrowTriangleFilledTip,
                "tip_height": 0.1,
                "tip_width": 0.1,
            },
        )
        unit = axes.get_x_unit_size()

        obj = Cylinder(
            radius=0.125 * unit,
            height=0.25 * unit,
            direction=UP,
            show_ends=True,
            fill_opacity=1,
        ).move_to(axes.c2p(0, 0.125, 0))
        obj_label = Text("The object", font_size=24)
        obj_label.move_to(axes.c2p(-0.4, 0.25, 0))
        self.add_fixed_in_frame_mobjects(obj_label)
        self.remove(obj_label)

        sensor_loc = Dot3D(point=axes.c2p(0, 0, 1))
        sensor_dir = Arrow(
            start=sensor_loc.get_center(),
            end=sensor_loc.get_center() - 0.25 * unit * OUT,
            buff=0,
        )
        robot_camera = VGroup(sensor_loc, sensor_dir)
        camera_label = Text("The RGB and depth sensors", font_size=24)
        camera_label.move_to(axes.c2p(0.75, 0.5, 0))
        self.add_fixed_in_frame_mobjects(camera_label)
        self.remove(camera_label)

        x_label = (
            axes.get_x_axis_label(Tex("x"))
            .move_to(axes.c2p(1, 0, 0))
            .shift(0.25 * RIGHT)
        )
        y_label = (
            axes.get_y_axis_label(Tex("y"))
            .move_to(axes.c2p(0, 1, 0))
            .shift(0.25 * UP)
            .rotate(-PI / 2, axis=OUT)
        )
        z_label = (
            axes.get_z_axis_label(Tex("z"))
            .move_to(axes.c2p(0, 0, 1))
            .shift(0.25 * unit * OUT)
            .rotate(-PI / 2, axis=RIGHT)
        )

        self.play(FadeIn(axes))
        self.add_fixed_orientation_mobjects(x_label, y_label, z_label)

        self.play(
            FadeIn(obj),
            FadeIn(robot_camera),
        )
        self.play(FadeIn(obj_label))
        obj_label_arrow = Arrow(start=axes.c2p(0.25, 0.25, -0.25), end=obj.get_center())
        self.play(GrowArrow(obj_label_arrow))

        self.wait()

        self.play(
            FadeOut(obj_label),
            FadeOut(obj_label_arrow),
        )

        self.play(FadeIn(camera_label))
        camera_label_arrow = Arrow(
            start=axes.c2p(0, 0.35, 1), end=sensor_loc.get_center()
        )
        self.play(GrowArrow(camera_label_arrow))

        self.wait()

        self.play(
            FadeOut(camera_label),
            FadeOut(camera_label_arrow),
        )

        sensor_loc_up_line = Line(start=axes.c2p(0, 0, 1), end=axes.c2p(0, 0.375, 1))
        sensor_dir_up_line = Line(
            start=axes.c2p(0, 0, 0.875), end=axes.c2p(0, 0.375, 0.875)
        )
        sensor_loc_down_line = Line(start=axes.c2p(0, 0.375, 1), end=axes.c2p(0, 0, 1))
        sensor_dir_down_line = Line(
            start=axes.c2p(0, 0.375, 0.875), end=axes.c2p(0, 0, 0.875)
        )

        self.play(FadeIn(translate_up))
        self.play(
            MoveAlongPath(sensor_loc, sensor_loc_up_line),
            MoveAlongPath(sensor_dir, sensor_dir_up_line),
            rate_func=linear,
            run_time=2,
        )

        self.remove(translate_up)
        self.play(FadeIn(translate_down))
        self.play(
            MoveAlongPath(sensor_loc, sensor_loc_down_line),
            MoveAlongPath(sensor_dir, sensor_dir_down_line),
            rate_func=linear,
            run_time=2,
        )

        self.remove(translate_down)
        self.play(FadeIn(orbit_left))
        self.play(
            Rotate(
                sensor_loc,
                angle=-PI / 4,
                axis=UP,
                about_point=ORIGIN,
                rate_func=linear,
                run_time=2,
            ),
            Rotate(
                sensor_dir,
                angle=-PI / 4,
                axis=UP,
                about_point=ORIGIN,
                rate_func=linear,
                run_time=2,
            ),
        )

        self.remove(orbit_left)
        self.play(FadeIn(orbit_right))
        self.play(
            Rotate(
                sensor_loc,
                angle=PI / 8,
                axis=UP,
                about_point=ORIGIN,
                rate_func=linear,
                run_time=1,
            ),
            Rotate(
                sensor_dir,
                angle=PI / 8,
                axis=UP,
                about_point=ORIGIN,
                rate_func=linear,
                run_time=1,
            ),
        )

        self.play(FadeOut(orbit_right))


class RobotWithPlatform(ThreeDScene):  # type: ignore[misc]  # noqa: D101
    def construct(self) -> None:  # noqa: D102, PLR0915
        translate_up = Text("TRANSLATE_UP", font_size=24)
        translate_up.to_corner(UR)
        self.add_fixed_in_frame_mobjects(translate_up)
        self.remove(translate_up)
        translate_down = Text("TRANSLATE_DOWN", font_size=24)
        translate_down.to_corner(UR)
        self.add_fixed_in_frame_mobjects(translate_down)
        self.remove(translate_down)
        orbit_left = Text("ORBIT_LEFT", font_size=24)
        orbit_left.to_corner(UR)
        self.add_fixed_in_frame_mobjects(orbit_left)
        self.remove(orbit_left)
        orbit_right = Text("ORBIT_RIGHT", font_size=24)
        orbit_right.to_corner(UR)
        self.add_fixed_in_frame_mobjects(orbit_right)
        self.remove(orbit_right)

        self.set_camera_orientation(
            phi=147 * DEGREES, theta=147 * DEGREES, gamma=-60 * DEGREES, zoom=0.9
        )
        axes = ThreeDAxes(
            x_range=[-1, 1, 0.25],
            y_range=[-1, 1, 0.25],
            z_range=[-1, 1, 0.25],
            x_length=config.frame_height * 0.9,
            y_length=config.frame_height * 0.9,
            z_length=config.frame_height * 0.9,
            x_axis_config={
                "tick_size": 0.05,
                "tip_shape": ArrowTriangleFilledTip,
                "tip_height": 0.1,
                "tip_width": 0.1,
            },
            y_axis_config={
                "tick_size": 0.05,
                "tip_shape": ArrowTriangleFilledTip,
                "tip_height": 0.1,
                "tip_width": 0.1,
            },
            z_axis_config={
                "tick_size": 0.05,
                "tip_shape": ArrowTriangleFilledTip,
                "tip_height": 0.1,
                "tip_width": 0.1,
            },
        )
        unit = axes.get_x_unit_size()

        platform = (
            Cylinder(
                radius=0.375 * unit,
                height=0.01 * unit,
                direction=UP,
                show_ends=True,
                fill_opacity=1,
            )
            .move_to(axes.c2p(0, 0, 0))
            .set_color(GRAY)
        )
        platform_label = Text("The platform", font_size=24)
        platform_label.move_to(axes.c2p(-0.4, 0.25, 0))
        self.add_fixed_in_frame_mobjects(platform_label)
        self.remove(platform_label)

        dot_obj = Cylinder(
            radius=0.125 * unit,
            height=0.25 * unit,
            direction=UP,
            show_ends=True,
            fill_opacity=1,
        ).move_to(axes.c2p(0, 0.125, 0))
        obj_label = Text("The object", font_size=24)
        obj_label.move_to(axes.c2p(-0.4, 0.25, 0))
        self.add_fixed_in_frame_mobjects(obj_label)
        self.remove(obj_label)

        sensor_loc = Dot3D(point=axes.c2p(0, 0, 1))
        sensor_dir = Arrow(
            start=sensor_loc.get_center(),
            end=sensor_loc.get_center() - 0.25 * unit * OUT,
            buff=0,
        )
        robot_camera = VGroup(sensor_loc, sensor_dir)
        camera_label = Text("The RGB and depth sensors", font_size=24)
        camera_label.move_to(axes.c2p(0.75, 0.5, 0))
        self.add_fixed_in_frame_mobjects(camera_label)
        self.remove(camera_label)

        x_label = (
            axes.get_x_axis_label(Tex("x"))
            .move_to(axes.c2p(1, 0, 0))
            .shift(0.25 * RIGHT)
        )
        y_label = (
            axes.get_y_axis_label(Tex("y"))
            .move_to(axes.c2p(0, 1, 0))
            .shift(0.25 * UP)
            .rotate(-PI / 2, axis=OUT)
        )
        z_label = (
            axes.get_z_axis_label(Tex("z"))
            .move_to(axes.c2p(0, 0, 1))
            .shift(0.25 * unit * OUT)
            .rotate(-PI / 2, axis=RIGHT)
        )

        self.play(FadeIn(axes))
        self.add_fixed_orientation_mobjects(x_label, y_label, z_label)

        self.play(
            FadeIn(platform),
            FadeIn(dot_obj),
            FadeIn(robot_camera),
        )
        self.play(FadeIn(obj_label))
        obj_label_arrow = Arrow(
            start=axes.c2p(0.25, 0.25, -0.25), end=dot_obj.get_center()
        )
        self.play(GrowArrow(obj_label_arrow))

        self.wait()

        self.play(
            FadeOut(obj_label),
            FadeOut(obj_label_arrow),
        )

        self.play(FadeIn(platform_label))
        platform_label_arrow = Arrow(
            start=axes.c2p(0.25, 0.25, -0.25), end=axes.c2p(0.125, 0, -0.25)
        )
        self.play(GrowArrow(platform_label_arrow))

        self.wait()

        self.play(
            FadeOut(platform_label),
            FadeOut(platform_label_arrow),
        )

        self.play(FadeIn(camera_label))
        camera_label_arrow = Arrow(
            start=axes.c2p(0, 0.35, 1), end=sensor_loc.get_center()
        )
        self.play(GrowArrow(camera_label_arrow))

        self.wait()

        self.play(
            FadeOut(camera_label),
            FadeOut(camera_label_arrow),
        )

        sensor_loc_up_line = Line(start=axes.c2p(0, 0, 1), end=axes.c2p(0, 0.375, 1))
        sensor_dir_up_line = Line(
            start=axes.c2p(0, 0, 0.875), end=axes.c2p(0, 0.375, 0.875)
        )
        sensor_loc_down_line = Line(start=axes.c2p(0, 0.375, 1), end=axes.c2p(0, 0, 1))
        sensor_dir_down_line = Line(
            start=axes.c2p(0, 0.375, 0.875), end=axes.c2p(0, 0, 0.875)
        )

        self.play(FadeIn(translate_up))
        self.play(
            MoveAlongPath(sensor_loc, sensor_loc_up_line),
            MoveAlongPath(sensor_dir, sensor_dir_up_line),
            rate_func=linear,
            run_time=2,
        )

        self.remove(translate_up)
        self.play(FadeIn(translate_down))
        self.play(
            MoveAlongPath(sensor_loc, sensor_loc_down_line),
            MoveAlongPath(sensor_dir, sensor_dir_down_line),
            rate_func=linear,
            run_time=2,
        )

        self.remove(translate_down)
        self.play(FadeIn(orbit_left))
        self.play(
            Rotate(
                dot_obj,
                angle=PI,
                axis=UP,
                about_point=ORIGIN,
                rate_func=linear,
                run_time=2,
            ),
            Rotate(
                platform,
                angle=PI,
                axis=UP,
                about_point=ORIGIN,
                rate_func=linear,
                run_time=2,
            ),
            Rotate(
                axes,
                angle=PI,
                axis=UP,
                about_point=ORIGIN,
                rate_func=linear,
                run_time=2,
            ),
            Rotate(
                x_label,
                angle=PI,
                axis=UP,
                about_point=ORIGIN,
                rate_func=linear,
                run_time=2,
            ),
            Rotate(
                z_label,
                angle=PI,
                axis=UP,
                about_point=ORIGIN,
                rate_func=linear,
                run_time=2,
            ),
        )

        self.play(FadeOut(orbit_left))
        self.play(FadeIn(orbit_right))
        self.play(
            Rotate(
                dot_obj,
                angle=-PI,
                axis=UP,
                about_point=ORIGIN,
                rate_func=linear,
                run_time=2,
            ),
            Rotate(
                platform,
                angle=-PI,
                axis=UP,
                about_point=ORIGIN,
                rate_func=linear,
                run_time=2,
            ),
            Rotate(
                axes,
                angle=-PI,
                axis=UP,
                about_point=ORIGIN,
                rate_func=linear,
                run_time=2,
            ),
            Rotate(
                x_label,
                angle=-PI,
                axis=UP,
                about_point=ORIGIN,
                rate_func=linear,
                run_time=2,
            ),
            Rotate(
                z_label,
                angle=-PI,
                axis=UP,
                about_point=ORIGIN,
                rate_func=linear,
                run_time=2,
            ),
        )

        self.play(FadeOut(orbit_right))


class UnitCircle(Scene):  # type: ignore[misc]  # noqa: D101
    def construct(self) -> None:  # noqa: D102
        axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=config.frame_height * 0.8,
            y_length=config.frame_height * 0.8,
            axis_config={
                "numbers_to_include": np.arange(-2, 3, 1),
                "font_size": 24,
                "tick_size": 0.1,
                "tip_height": 0.1,
                "tip_width": 0.1,
            },
        )
        unit = axes.get_x_unit_size()
        z_label = axes.get_x_axis_label(Tex("z"))
        x_label = axes.get_y_axis_label(Tex("x"))
        self.play(FadeIn(axes), FadeIn(z_label), FadeIn(x_label))

        notes = Text(
            "Looking at the robot setup\nfrom the top.",
            font_size=24,
        )
        notes.to_corner(UR)
        self.play(Write(notes))

        self.wait(2)

        unit_circle = Circle(radius=unit, color=WHITE, stroke_width=2)
        unit_circle_text = Text(
            "Consider the ZX unit circle.",
            font_size=24,
        )
        unit_circle_text.to_corner(UR)
        self.remove(notes)
        self.play(Create(unit_circle), Write(unit_circle_text))

        self.wait(2)

        obj = Circle(
            radius=0.125 * unit,
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=1,
        )
        obj_text = Text(
            "The object is placed\nat (0, 0, 0), the origin.",
            font_size=24,
        )
        obj_text.to_corner(UR)
        self.remove(unit_circle_text)
        self.play(DrawBorderThenFill(obj), Write(obj_text))

        self.wait(2)

        sensor = Dot(point=unit * RIGHT, color=WHITE)
        sensor_dir = Arrow(
            start=sensor.get_center(),
            end=sensor.get_center() - 0.25 * unit * RIGHT,
            buff=0,
        )
        sensor_text = Text(
            "The sensor is located\nat (0, 0, 1).",
            font_size=24,
        )
        sensor_text.to_corner(UR)
        self.remove(obj_text)
        self.play(FadeIn(sensor), FadeIn(sensor_dir), Write(sensor_text))

        self.wait(2)

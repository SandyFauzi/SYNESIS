"""Empat loop visual Manim untuk video Bulan 1 sesi 1-4."""

from __future__ import annotations

import numpy as np
from manim import (
    AnimationGroup,
    Arrow,
    Axes,
    BLUE_C,
    BLUE_E,
    Circle,
    Create,
    DashedLine,
    Dot,
    DOWN,
    FadeIn,
    FadeOut,
    GREEN_A,
    GREEN_C,
    GREY_B,
    GREY_D,
    GrowFromCenter,
    LaggedStart,
    LEFT,
    Line,
    MathTex,
    ORANGE,
    ORIGIN,
    PI,
    RED_C,
    RIGHT,
    RoundedRectangle,
    Scene,
    Square,
    Text,
    Transform,
    UP,
    VGroup,
    WHITE,
    YELLOW,
    config,
    linear,
)


config.pixel_width = 720
config.pixel_height = 720
config.frame_width = 8
config.frame_height = 8
config.frame_rate = 30
config.background_color = "#08080C"

INK = "#E8EDF2"
MUTED = "#717784"
GREEN = "#37E68A"
PANEL = "#11151C"
PURPLE = "#9977FF"


def title(text: str, subtitle: str) -> VGroup:
    heading = Text(text, font="Arial", weight="BOLD", font_size=34, color=INK)
    note = Text(subtitle, font="Arial", font_size=18, color=MUTED)
    group = VGroup(heading, note).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.32)
    return group


def badge(text: str, color: str = GREEN) -> VGroup:
    box = RoundedRectangle(corner_radius=0.12, width=1.45, height=0.43)
    box.set_fill(color, opacity=0.12).set_stroke(color, opacity=0.65, width=1.4)
    label = Text(text, font="Consolas", font_size=16, color=color)
    return VGroup(box, label)


class Sesi1(Scene):
    """Forward graph lalu denyut gradien bergerak mundur."""

    def construct(self) -> None:
        header = title("SESI 1 · AUTOGRAD", "nilai maju → gradien mundur")
        labels = ["a", "b", "×", "c", "+", "loss"]
        xs = [-3.15, -2.0, -0.8, 0.35, 1.55, 2.8]
        ys = [-0.9, 0.9, 0.0, -0.9, 0.0, 0.0]
        colors = [BLUE_C, BLUE_C, PURPLE, BLUE_C, PURPLE, GREEN]
        nodes = VGroup()
        for label, x, y, color in zip(labels, xs, ys, colors):
            node = Circle(radius=0.38).set_fill(color, opacity=0.16).set_stroke(color, width=2)
            text = Text(label, font="Consolas", font_size=21, color=INK)
            nodes.add(VGroup(node, text).move_to([x, y, 0]))

        pairs = [(0, 2), (1, 2), (2, 4), (3, 4), (4, 5)]
        arrows = VGroup(
            *[
                Arrow(nodes[a].get_center(), nodes[b].get_center(), buff=0.43,
                      stroke_width=2.5, color=GREY_D, max_tip_length_to_length_ratio=0.13)
                for a, b in pairs
            ]
        )
        forward = badge("FORWARD", BLUE_C).move_to([-1.8, -2.45, 0])
        backward = badge("BACKWARD", GREEN).move_to([1.8, -2.45, 0])
        values = VGroup(
            *[
                Text(v, font="Consolas", font_size=16, color=GREY_B).next_to(nodes[i], DOWN, buff=0.1)
                for i, v in enumerate(["2.0", "−3.0", "−6.0", "10.0", "4.0", "4.0"])
            ]
        )

        self.play(FadeIn(header), FadeIn(forward), run_time=0.7)
        self.play(LaggedStart(*[GrowFromCenter(n) for n in nodes], lag_ratio=0.12), run_time=1.0)
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.13), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(v, shift=UP * 0.08) for v in values], lag_ratio=0.1), run_time=0.8)
        self.play(FadeOut(forward), FadeIn(backward), run_time=0.5)

        reverse_order = [4, 3, 2, 1, 0]
        for index in reverse_order:
            pulse = arrows[index].copy().set_color(GREEN).set_stroke(width=6)
            self.play(Create(pulse), nodes[pairs[index][0]][0].animate.set_stroke(GREEN, width=4), run_time=0.65)
            self.play(FadeOut(pulse), run_time=0.15)

        gradients = VGroup(
            *[
                Text(g, font="Consolas", font_size=15, color=GREEN).next_to(nodes[i], UP, buff=0.1)
                for i, g in enumerate(["g=−3", "g=2", "g=1", "g=1", "g=1", "g=1"])
            ]
        )
        self.play(LaggedStart(*[FadeIn(g, shift=DOWN * 0.08) for g in gradients], lag_ratio=0.08), run_time=0.7)
        self.wait(0.5)


class Sesi2(Scene):
    """Data mengalir melalui MLP dan ReLU."""

    def construct(self) -> None:
        header = title("SESI 2 · MLP", "fitur → neuron → keputusan")
        layer_x = [-2.8, -1.05, 0.8, 2.75]
        layer_counts = [3, 5, 4, 2]
        layer_colors = [BLUE_C, PURPLE, ORANGE, GREEN]
        layers = VGroup()
        for x, count, color in zip(layer_x, layer_counts, layer_colors):
            column = VGroup()
            for y in np.linspace(-1.65, 1.35, count):
                column.add(Circle(radius=0.18).set_fill(color, opacity=0.18).set_stroke(color, width=1.7).move_to([x, y, 0]))
            layers.add(column)

        edges = VGroup()
        for left, right in zip(layers[:-1], layers[1:]):
            for a in left:
                for b in right:
                    edges.add(Line(a.get_center(), b.get_center(), color="#28303B", stroke_width=1.0))

        names = VGroup(
            *[
                Text(name, font="Consolas", font_size=15, color=MUTED).next_to(layer, DOWN, buff=0.25)
                for name, layer in zip(["INPUT", "LAYER 1", "RELU", "OUTPUT"], layers)
            ]
        )
        relu_axes = Axes(
            x_range=[-1, 1, 1], y_range=[0, 1, 1], x_length=1.15, y_length=0.75,
            axis_config={"color": GREY_D, "stroke_width": 1.5, "include_ticks": False},
        ).move_to([0.8, -2.55, 0])
        relu_curve = VGroup(
            Line(relu_axes.c2p(-1, 0), relu_axes.c2p(0, 0), color=GREEN, stroke_width=4),
            Line(relu_axes.c2p(0, 0), relu_axes.c2p(1, 1), color=GREEN, stroke_width=4),
        )
        relu_label = Text("max(0, x)", font="Consolas", font_size=15, color=GREEN).next_to(relu_axes, RIGHT, buff=0.18)

        self.play(FadeIn(header), run_time=0.7)
        self.play(FadeIn(edges), LaggedStart(*[FadeIn(layer) for layer in layers], lag_ratio=0.15), run_time=1.2)
        self.play(FadeIn(names), Create(relu_axes), Create(relu_curve), FadeIn(relu_label), run_time=0.8)

        for step in range(3):
            pulses = VGroup()
            for x, color in zip(layer_x, layer_colors):
                y = [-0.9, 0.1, 0.85][step]
                pulses.add(Dot([x, y, 0], radius=0.11, color=color).set_glow_factor(0.6))
            self.play(
                LaggedStart(*[GrowFromCenter(p) for p in pulses], lag_ratio=0.18),
                layers[(step + 1) % len(layers)].animate.set_stroke(GREEN, width=2.5),
                run_time=0.65,
            )
            self.play(FadeOut(pulses), run_time=0.2)

        loss = badge("LOSS ↓", GREEN).move_to([2.7, -2.55, 0])
        self.play(FadeIn(loss, shift=UP * 0.15), run_time=0.5)
        self.play(
            AnimationGroup(
                *[layer.animate.set_fill(GREEN, opacity=0.12) for layer in layers],
                lag_ratio=0.12,
            ),
            run_time=1.0,
        )
        self.play(
            AnimationGroup(
                *[layer.animate.set_fill(layer_colors[i], opacity=0.18) for i, layer in enumerate(layers)],
                lag_ratio=0.12,
            ),
            run_time=1.0,
        )
        self.wait(0.8)


class Sesi34(Scene):
    """Digit menjadi probabilitas; backward memakai tumpukan, bukan rekursi."""

    DIGIT = (
        "0011100",
        "0110110",
        "1100011",
        "0000110",
        "0001100",
        "0011000",
        "0111111",
    )

    def construct(self) -> None:
        header = title("SESI 3 · MNIST", "softmax + backward tanpa tembok rekursi")
        pixels = VGroup()
        for row, bits in enumerate(self.DIGIT):
            for col, bit in enumerate(bits):
                square = Square(side_length=0.25, stroke_width=0.5, stroke_color="#242A34")
                square.set_fill(INK if bit == "1" else "#141820", opacity=1)
                square.move_to([-2.8 + col * 0.25, 1.05 - row * 0.25, 0])
                pixels.add(square)

        arrow = Arrow([-0.85, 0.3, 0], [0.05, 0.3, 0], buff=0.05, color=MUTED)
        bars = VGroup()
        values = [0.04, 0.03, 0.05, 0.08, 0.09, 0.06, 0.05, 0.07, 0.46, 0.07]
        for i, value in enumerate(values):
            bar = RoundedRectangle(corner_radius=0.04, width=3.0 * value + 0.04, height=0.25)
            color = GREEN if i == 8 else BLUE_E
            bar.set_fill(color, opacity=0.85).set_stroke(color, width=0)
            bar.move_to([0.25 + bar.width / 2, 1.55 - i * 0.34, 0])
            number = Text(str(i), font="Consolas", font_size=13, color=MUTED).next_to(bar, LEFT, buff=0.1)
            bars.add(VGroup(bar, number))

        brace_text = Text("Σ peluang = 1", font="Consolas", font_size=16, color=GREEN).move_to([1.8, -2.1, 0])
        wall = DashedLine([-3.4, -2.65, 0], [3.4, -2.65, 0], color=RED_C, dash_length=0.12)
        wall_label = Text("batas rekursi", font="Consolas", font_size=14, color=RED_C).next_to(wall, DOWN, buff=0.08)
        stack = VGroup()
        for i, label in enumerate(["loss", "+", "×", "relu", "w"]):
            block = RoundedRectangle(corner_radius=0.07, width=1.15, height=0.34)
            block.set_fill(PANEL, opacity=1).set_stroke(GREEN, opacity=0.65)
            txt = Text(label, font="Consolas", font_size=14, color=INK)
            stack.add(VGroup(block, txt).move_to([-2.4 + i * 1.2, -2.25, 0]))

        self.play(FadeIn(header), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(p) for p in pixels], lag_ratio=0.01), run_time=0.9)
        self.play(Create(arrow), LaggedStart(*[GrowFromCenter(b) for b in bars], lag_ratio=0.06), run_time=1.2)
        self.play(FadeIn(brace_text), run_time=0.5)
        self.play(Create(wall), FadeIn(wall_label), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.12) for b in stack], lag_ratio=0.12), run_time=1.1)
        for i in range(len(stack) - 1, -1, -1):
            self.play(stack[i][0].animate.set_fill(GREEN, opacity=0.32), run_time=0.35)
        self.play(wall.animate.set_color(GREEN), wall_label.animate.set_color(GREEN), run_time=0.6)
        solved = badge("ITERATIF ✓", GREEN).move_to([2.45, -3.05, 0])
        self.play(FadeIn(solved), run_time=0.5)
        self.wait(0.45)


class Sesi4(Scene):
    """Operasi Tensor dan lintasan beberapa optimizer."""

    def construct(self) -> None:
        header = title("SESI 4 · TENSOR", "matriks + optimizer menuju loss minimum")
        matrix_a = self.matrix_grid(2, 3, BLUE_C).move_to([-2.7, 1.05, 0])
        matrix_b = self.matrix_grid(3, 2, PURPLE).move_to([-0.5, 1.05, 0])
        matrix_c = self.matrix_grid(2, 2, GREEN).move_to([2.15, 1.05, 0])
        at = Text("@", font="Consolas", font_size=32, color=MUTED).move_to([-1.65, 1.05, 0])
        eq = Text("=", font="Consolas", font_size=28, color=MUTED).move_to([0.75, 1.05, 0])

        axes = Axes(
            x_range=[-3, 3, 1], y_range=[0, 5, 1], x_length=6.2, y_length=2.8,
            axis_config={"color": GREY_D, "stroke_width": 1.2, "include_ticks": False},
        ).move_to([0, -1.4, 0])
        valley = axes.plot(lambda x: 0.45 * x * x + 0.2, x_range=[-2.8, 2.8], color=GREY_B, stroke_width=3)
        minimum = Dot(axes.c2p(0, 0.2), radius=0.09, color=GREEN)
        minimum_label = Text("min loss", font="Consolas", font_size=14, color=GREEN).next_to(minimum, DOWN, buff=0.08)
        labels = VGroup(
            Text("SGD", font="Consolas", font_size=13, color=BLUE_C).move_to([-2.65, -0.1, 0]),
            Text("Momentum", font="Consolas", font_size=13, color=ORANGE).move_to([-1.25, -0.1, 0]),
            Text("Adam", font="Consolas", font_size=13, color=GREEN).move_to([1.9, -0.1, 0]),
        )

        paths = [
            ([2.5, 1.7, 1.05, 0.58, 0.27, 0.08, 0.0], BLUE_C),
            ([-2.6, -1.35, -0.35, 0.32, -0.12, 0.04, 0.0], ORANGE),
            ([2.2, 1.15, 0.48, 0.14, 0.02, 0.0], GREEN),
        ]

        self.play(FadeIn(header), run_time=0.7)
        self.play(FadeIn(matrix_a), FadeIn(matrix_b), FadeIn(at), run_time=0.8)
        self.play(FadeIn(eq), Transform(matrix_a.copy(), matrix_c), run_time=1.0)
        self.play(Create(axes), Create(valley), FadeIn(minimum), FadeIn(minimum_label), FadeIn(labels), run_time=1.1)

        for points, color in paths:
            dots = VGroup(*[Dot(axes.c2p(x, 0.45 * x * x + 0.2), radius=0.07, color=color) for x in points])
            route = VGroup(*[Line(dots[i].get_center(), dots[i + 1].get_center(), color=color, stroke_width=2.5) for i in range(len(dots) - 1)])
            self.play(LaggedStart(*[FadeIn(d) for d in dots], *[Create(line) for line in route], lag_ratio=0.08), run_time=1.15)

        tensor = badge("grad → update", GREEN).move_to([0, -3.25, 0])
        self.play(FadeIn(tensor), minimum.animate.scale(1.7), run_time=0.55)
        self.play(minimum.animate.scale(1 / 1.7), run_time=0.35)
        self.wait(0.25)

    @staticmethod
    def matrix_grid(rows: int, cols: int, color: str) -> VGroup:
        cells = VGroup()
        for row in range(rows):
            for col in range(cols):
                cell = Square(side_length=0.31, stroke_color=color, stroke_width=1.2)
                cell.set_fill(color, opacity=0.12 + 0.08 * ((row + col) % 2))
                cell.move_to([col * 0.32, -row * 0.32, 0])
                cells.add(cell)
        cells.center()
        return cells

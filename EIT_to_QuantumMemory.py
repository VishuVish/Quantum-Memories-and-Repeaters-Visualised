from manim import *
import numpy as np

class EITMemoryLambda(Scene):
    def construct(self):

        # -----------------------------
        # TRACKERS
        # -----------------------------
        control = ValueTracker(1.0)      # Control Rabi frequency (normalized)
        pulse_z = ValueTracker(-4.0)     # Probe pulse position

        def photonic_part():
            return control.get_value()**2

        def spin_part():
            return 1 - control.get_value()**2

        # -----------------------------
        # TITLE
        # -----------------------------
        title = Text(
            "EIT Quantum Memory (Λ System)",
            font_size=32
        ).to_edge(UP)
        self.add(title)

        # ======================================================
        # LEFT SIDE: Λ-TYPE THREE LEVEL SYSTEM
        # ======================================================
        atom_center = LEFT*4 + DOWN*0.3

        # Energy levels (Λ geometry)
        g1_y = -1.9   # |1>
        g2_y = -1.3   # |2>
        e3_y =  1.2   # |3>

        g1 = Line(atom_center + LEFT*0.9 + UP*g1_y,
                  atom_center + LEFT*0.1 + UP*g1_y)
        g2 = Line(atom_center + RIGHT*0.1 + UP*g2_y,
                  atom_center + RIGHT*0.9 + UP*g2_y)
        e3 = Line(atom_center + LEFT*0.6 + UP*e3_y,
                  atom_center + RIGHT*0.6 + UP*e3_y)

        lbl1 = MathTex("|1\\rangle").next_to(g1, LEFT)
        lbl2 = MathTex("|2\\rangle").next_to(g2, RIGHT)
        lbl3 = MathTex("|3\\rangle").next_to(e3, UP)

        self.add(g1, g2, e3, lbl1, lbl2, lbl3)

        # -----------------------------
        # TRANSITIONS
        # -----------------------------
        probe_arrow = always_redraw(
            lambda: Arrow(
                g1.get_center(), e3.get_center(),
                buff=0.1,
                color=RED,
                stroke_width=6
            ).set_opacity(photonic_part())
        )

        control_arrow = always_redraw(
            lambda: Arrow(
                g2.get_center(), e3.get_center(),
                buff=0.1,
                color=BLUE,
                stroke_width=6
            ).set_opacity(control.get_value())
        )

        # Ground-state coherence (spin wave)
        spin_coherence = always_redraw(
            lambda: DashedLine(
                g1.get_center(),
                g2.get_center(),
                dash_length=0.15,
                color=GREEN,
                stroke_width=5
            ).set_opacity(spin_part())
        )

        self.add(probe_arrow, control_arrow, spin_coherence)

        # Labels
        self.add(
            Text("Probe", color=RED, font_size=16).next_to(probe_arrow, LEFT),
            Text("Control", color=BLUE, font_size=16).next_to(control_arrow, RIGHT),
            Text("Spin-wave coherence", color=GREEN, font_size=16)
                .next_to(spin_coherence, DOWN)
        )

        # ======================================================
        # RIGHT SIDE: PROPAGATION / STORAGE PICTURE
        # ======================================================
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[0, 1.2, 0.5],
            x_length=7,
            y_length=3,
            axis_config={"include_tip": False}
        ).shift(RIGHT*2 + DOWN*0.3)

        self.add(axes)

        def gaussian(x, mu):
            return np.exp(-2*(x - mu)**2)

        probe_wave = always_redraw(
            lambda: axes.plot(
                lambda x: photonic_part()*gaussian(x, pulse_z.get_value()),
                color=RED,
                stroke_width=4
            )
        )

        spin_wave = always_redraw(
            lambda: axes.plot(
                lambda x: spin_part()*gaussian(x, 0),
                color=GREEN,
                stroke_width=4
            )
        )

        self.add(probe_wave, spin_wave)

        # -----------------------------
        # AXIS LABELS (PHYSICALLY CORRECT)
        # -----------------------------
        x_label = Text(
            "Position inside medium (z)",
            font_size=16
        ).next_to(axes.x_axis, DOWN)    
        y_label = Text(
        r"Psi(z)",
        font_size=16
        ).next_to(axes.y_axis, UP)

        self.add(x_label, y_label)

        # -----------------------------
        # CONTROL INDICATOR
        # -----------------------------
        control_bar = always_redraw(
            lambda: Rectangle(
                width=2.5*control.get_value(),
                height=0.25,
                fill_color=BLUE,
                fill_opacity=0.8,
                stroke_width=0
            ).to_corner(UR).shift(DOWN*0.8 + LEFT*0.3)
        )

        self.add(
            control_bar,
            Text("Control Ωc", font_size=16, color=BLUE)
                .next_to(control_bar, DOWN)
        )

        # ======================================================
        # ANIMATION SEQUENCE
        # ======================================================

        # Probe enters
        self.play(
            pulse_z.animate.set_value(0),
            run_time=3,
            rate_func=linear
        )

        # Slow-light regime (50/50 polariton)
        self.play(
            control.animate.set_value(0.7),
            run_time=2
        )

        # Storage (mapping to spin wave)
        self.play(
            control.animate.set_value(0.0),
            run_time=2
        )

        store_text = Text(
            "Probe photon mapped to ground-state coherence",
            font_size=24,
            color=GREEN
        ).to_edge(DOWN)

        self.play(FadeIn(store_text))
        self.wait(1.5)
        self.play(FadeOut(store_text))

        # Retrieval
        self.play(
            control.animate.set_value(1.0),
            run_time=2
        )

        self.play(
            pulse_z.animate.set_value(4),
            run_time=3,
            rate_func=linear
        )

        self.wait()

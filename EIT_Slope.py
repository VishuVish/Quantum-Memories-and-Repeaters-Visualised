from manim import *
import numpy as np

class EITSlopeVariation(Scene):
    def construct(self):
        # ============================
        # 1. PHYSICS DEFINITIONS
        # ============================
        def lorentzian_base(x, center, width):
            return 1 / ((x - center)**2 + width**2)

        def dispersive_base(x, center, width):
            return -1 * (x - center) / ((x - center)**2 + width**2)

        CENTER_FREQ = 3.0  
        GAMMA = 0.3        
        AMP_SCALE = 0.2    

        window_splitter = ValueTracker(2.0)

        def get_current_absorption(x):
            split_amt = window_splitter.get_value() / 2.0
            return AMP_SCALE * (lorentzian_base(x, CENTER_FREQ - split_amt, GAMMA) + \
                                lorentzian_base(x, CENTER_FREQ + split_amt, GAMMA))

        def get_current_dispersion(x):
            split_amt = window_splitter.get_value() / 2.0
            return AMP_SCALE * (dispersive_base(x, CENTER_FREQ - split_amt, GAMMA) + \
                                dispersive_base(x, CENTER_FREQ + split_amt, GAMMA))

        # ============================
        # 2. AXES SETUP
        # ============================
        ax_left = Axes(
            x_range=[0, 6, 1], y_range=[0, 4, 2],
            x_length=5, y_length=3.5,
            axis_config={"include_tip": False, "color": GREY},
        ).to_edge(LEFT, buff=1.0).shift(UP*0.5)

        x_lbl_left = MathTex(r"\text{Detuning } \Delta", font_size=20).next_to(ax_left.x_axis, RIGHT, buff=0.2)
        y_lbl_left = Text("Absorption", font_size=16).next_to(ax_left.y_axis, UP)


        ax_right = Axes(
            x_range=[0, 6, 1], y_range=[-3, 3, 1.5],
            x_length=5, y_length=3.5,
            axis_config={"include_tip": False, "color": GREY},
        ).to_edge(RIGHT, buff=1.0).shift(UP*0.5)

        x_lbl_right = Text("Frequency", font_size=16).next_to(ax_right.x_axis.get_end(), UP, buff=0.2)
        y_lbl_right = Text("Dispersion", font_size=16).next_to(ax_right.y_axis, UP)

        lbl_left = Text("Absorption (Window Width)", font_size=24, color=GREEN).next_to(ax_left, UP*2.5)
        lbl_right = Text("Slope (Kramers-Kronig)", font_size=24, color=BLUE).next_to(ax_right, UP*2.5)
        
        center_line_L = DashedLine(
            start=ax_left.c2p(CENTER_FREQ, 0), end=ax_left.c2p(CENTER_FREQ, 4), 
            color=GREY, stroke_opacity=0.5
        )
        center_line_R = DashedLine(
            start=ax_right.c2p(CENTER_FREQ, -3), end=ax_right.c2p(CENTER_FREQ, 3), 
            color=GREY, stroke_opacity=0.5
        )

        # ============================
        # 3. DYNAMIC PLOTS
        # ============================
        graph_abs = always_redraw(lambda: ax_left.plot(
            get_current_absorption, x_range=[0.1, 5.9], color=GREEN, stroke_width=4
        ))

        graph_disp = always_redraw(lambda: ax_right.plot(
            get_current_dispersion, x_range=[0.1, 5.9], color=BLUE, stroke_width=4
        ))

        slope_highlight = always_redraw(lambda: ax_right.plot(
            get_current_dispersion, 
            x_range=[CENTER_FREQ - 0.15, CENTER_FREQ + 0.15], 
            color=RED, stroke_width=8
        ))

        # ============================
        # 4. INDICATORS (FIXED POWER BAR)
        # ============================
        power_bar_bg = Rectangle(width=6, height=0.3, color=WHITE, fill_opacity=0.1).to_edge(DOWN, buff=1.5)
        power_label = Text("Control Laser Power (|Ωc|²)", font_size=20).next_to(power_bar_bg, UP)
        
        # FIXED: We use .move_to(power_bar_bg.get_left()) and .shift(RIGHT * new_width/2)
        # This ensures it grows/shrinks from the left edge of the container
        power_bar_fill = always_redraw(lambda: Rectangle(
            width=max(0.01, 6 * (window_splitter.get_value() / 2.0)), 
            height=0.3, 
            color=RED, fill_opacity=0.8, stroke_width=0
        ).move_to(power_bar_bg.get_left(), aligned_edge=LEFT))

       
        mid_arrow = Arrow(start=LEFT, end=RIGHT, color=YELLOW, stroke_width=6).move_to(ORIGIN).shift(UP*0.5)
        kk_label = Text("Kramers-Kronig", font_size=16, color=YELLOW).next_to(mid_arrow, UP)

        # ============================
        # 5. ANIMATION
        # ============================
        self.add(ax_left, ax_right, lbl_left, lbl_right, center_line_L, center_line_R,
                 x_lbl_left, y_lbl_left, x_lbl_right, y_lbl_right)
        self.add(graph_abs, graph_disp, slope_highlight)
        self.add(power_bar_bg, power_label, power_bar_fill)
        self.add(mid_arrow, kk_label)

        self.wait(1)
        # Squeeze the window - Power goes down, slope goes up
        self.play(
            window_splitter.animate.set_value(0.3), 
            run_time=6,
            rate_func=slow_into
        )
        self.wait(2)
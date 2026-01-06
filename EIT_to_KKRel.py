from manim import *
import numpy as np

class EIT_Static_Slide(Scene):
    def construct(self):
        # --- 1. DEFINE PHYSICS FUNCTIONS ---
        def lorentzian(x, center, width, height):
            return height * (width**2 / ((x - center)**2 + width**2))

        def dispersive_func(x, center, width, height):
            return -1 * height * 0.5 * (width * (x - center)) / ((x - center)**2 + width**2)

        center_freq = 2.5
        split_width = 0.8
        gamma = 0.4
        amp = 1.0

        def eit_absorption(x):
            return lorentzian(x, center_freq - split_width, gamma, amp) + \
                   lorentzian(x, center_freq + split_width, gamma, amp)

        def eit_dispersion(x):
            return dispersive_func(x, center_freq - split_width, gamma, amp) + \
                   dispersive_func(x, center_freq + split_width, gamma, amp)

        # --- 2. LAYOUT & AXES ---
        
        # LEFT: Absorption Graph
        ax_left = Axes(
            x_range=[0, 5, 1], y_range=[0, 1.5, 0.5],
            x_length=5, y_length=3.5,
            axis_config={"include_tip": False, "color": GREY},
        ).to_edge(LEFT, buff=1.0).shift(UP*0.5)

        x_lbl_left = MathTex(r"\text{Detuning } \Delta", font_size=20).next_to(ax_left.x_axis, RIGHT, buff=0.2)
        y_lbl_left = Text("Absorption", font_size=16).next_to(ax_left.y_axis, UP)

        # RIGHT: Dispersion Graph
        # Shifted LEFT by 0.5 to keep labels in frame
        ax_right = Axes(
            x_range=[0, 5, 1], y_range=[-0.8, 0.8, 0.4],
            x_length=5, y_length=3.5,
            axis_config={"include_tip": False, "color": GREY},
        ).to_edge(RIGHT, buff=1.0).shift(UP*0.5) 
        
        # Fixed: Label is now BELOW the axis tip, ensuring it's in frame
        x_lbl_right = Text("Frequency", font_size=16).next_to(ax_right.x_axis.get_end(), UP, buff=0.2)
        y_lbl_right = Text("Dispersion", font_size=16).next_to(ax_right.y_axis, UP)

        # --- 3. PLOTS ---
        curve_abs = ax_left.plot(eit_absorption, color=GREEN, stroke_width=4)
        curve_disp = ax_right.plot(eit_dispersion, color=BLUE, stroke_width=4)

        # --- 4. HIGHLIGHTS & LABELS ---

        # Left Title
        lbl_left = Text("EIT Absorption", font_size=32, color=GREEN).next_to(ax_left, UP)
        sub_left = Text("(Transparency Window)", font_size=20, color=WHITE).next_to(lbl_left, DOWN*0.5)

        # Right Title
        lbl_right = Text("Kramers-Kronig Dispersion", font_size=20, color=BLUE).next_to(ax_right, UP*2)
        
        # The "Slope" Highlight
        slope_highlight = ax_right.plot(
            eit_dispersion, 
            x_range=[2.2, 2.8],
            color=RED, 
            stroke_width=8
        )
        
        # FIXED: Vertical Label and Arrow
        slope_label = Text("Steep Positive Slope", font_size=14, color=RED).next_to(slope_highlight, UP, buff=0.5)
        slope_arrow = Arrow(
            start=slope_label.get_bottom(), 
            end=slope_highlight.get_center(), 
            color=RED, 
            buff=0.1, 
            stroke_width=3,
            max_tip_length_to_length_ratio=0.3
        )
        
        # The Connecting Arrow in the Middle
        mid_arrow = Arrow(
            start=ax_left.get_right() + RIGHT*0.2, 
            end=ax_right.get_left() + LEFT*0.2, 
            color=WHITE, 
            stroke_width=6,
            buff=0.1
        )
        
        # --- 5. KRAMERS-KRONIG IMPLICATION MARKER ---
        connection_color = YELLOW

        # Get coordinates of the "Dip" (Left) and the "Slope" (Right)
        target_dip = ax_left.c2p(center_freq, eit_absorption(center_freq))
        target_slope = ax_right.c2p(center_freq, 0)

        # Define how low the connector lines drop
        connector_y_level = ax_left.get_bottom()[1] - 0.6

        # Define the corners for the "U" shape connector
        corner_L = np.array([target_dip[0], connector_y_level, 0])
        corner_R = np.array([target_slope[0], connector_y_level, 0])

        # Create the dashed connection lines
        h_line = DashedLine(start=corner_L, end=corner_R, color=connection_color)
        v_line_L = DashedLine(start=corner_L, end=target_dip + DOWN*0.05, color=connection_color)
        v_line_L.add_tip(tip_length=0.15)
        v_line_R = DashedLine(start=corner_R, end=target_slope + DOWN*0.05, color=connection_color)
        v_line_R.add_tip(tip_length=0.15)

        # THE IMPLICATION TEXT
        # We split it into two logical parts to make it readable
        implication_text = MathTex(
            r"\frac {d\chi''}{d\omega} \implies \frac{dn}{d\omega} \to \infty",
            color=connection_color,
            font_size=36
        ).next_to(h_line, DOWN, buff=0.1)

        # Optional: Add a text describing the result (Slow Light) below it
        slow_light_text = Text(
            "(Slow Light Condition)",
            color=YELLOW_B,
            font_size=16
        ).next_to(implication_text, DOWN, buff=0.1)

        # --- 6. RENDER STATIC SCENE ---
        self.add(
            ax_left, curve_abs, lbl_left, sub_left,
            mid_arrow,
            ax_right, curve_disp, lbl_right,
            slope_highlight, slope_label, slope_arrow,
            x_lbl_left, y_lbl_left, x_lbl_right, y_lbl_right,
            h_line, v_line_L, v_line_R,
            implication_text, slow_light_text  # Added the new labels here
        )
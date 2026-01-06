from manim import *
import numpy as np

class EIT_Final_Fixed(Scene):
    def construct(self):
        # --- SETUP & HELPERS ---
        def lorentzian(x, center, width, height):
            return height * (width**2 / ((x - center)**2 + width**2))
        
        # EIT Profile for Phase 3
        def eit_profile(x):
            return lorentzian(x, 2.5 - 0.8, 0.4, 0.6) + lorentzian(x, 2.5 + 0.8, 0.4, 0.6)

        # --- LAYOUT CONSTANTS ---
        atom_center = LEFT * 3.5
        graph_origin = RIGHT * 3 
        
        # Scale for mapping Frequency (x-axis) to Energy Level Height (y-axis)
        energy_scale = 0.6 / 0.8 

        # ==========================================
        #        PHASE 1: NORMAL ABSORPTION
        # ==========================================
        
        # 1. Title
        title = Text("Phase 1: Normal Absorption", font_size=28, color=YELLOW).to_edge(UP)

        # 2. Static Objects
        g_initial = Line(atom_center + LEFT*1, atom_center + RIGHT*1, color=WHITE).shift(DOWN * 2)
        lbl1 = MathTex("|1\\rangle").next_to(g_initial, LEFT)

        e3_solid = Line(atom_center + LEFT*1 + UP*1.5, atom_center + RIGHT*1 + UP*1.5, color=GRAY) 
        lbl3 = MathTex("|3\\rangle").next_to(e3_solid, UP)

        probe_arrow = Arrow(g_initial.get_center(), e3_solid.get_center(), color=RED, buff=0.1, stroke_width=4)
        probe_lbl = Text("Probe", color=RED, font_size=18).next_to(probe_arrow, LEFT, buff=0.1)

        # 3. Graph
        axes = Axes(
            x_range=[0, 5, 1], y_range=[0, 1.2, 0.5],
            x_length=5, y_length=3.5,
            axis_config={"include_tip": True},
        ).move_to(graph_origin)
        
        axes_lbl = Text("Absorption", font_size=20).next_to(axes, UP)
        
        # Initial X-Label (Frequency)
        x_lbl = Text("Frequency", font_size=16).next_to(axes.x_axis, RIGHT)
        y_lbl = Text("Absorption", font_size=16).next_to(axes.y_axis, UP)

        curve_data_1 = lambda x: lorentzian(x, 2.5, 0.6, 1.0)
        curve_single = axes.plot(curve_data_1, color=RED)

        # --- ANIMATION PHASE 1 ---
        self.play(Write(title))
        self.play(Create(g_initial), Write(lbl1), Create(e3_solid), Write(lbl3))
        self.play(GrowFromCenter(probe_arrow), Write(probe_lbl))
        self.play(Create(axes), Write(axes_lbl), Write(x_lbl), Write(y_lbl))
        self.play(Create(curve_single), run_time=2)
        self.wait(1)

        # ==========================================
        #    PHASE 2: TRANSITION TO LAMBDA & SPLITTING
        # ==========================================
        
        title_phase2 = Text("Phase 2: Control On (Splitting)", font_size=28, color=BLUE).to_edge(UP)

        # Target Positions
        g1_target = Line(atom_center + LEFT*1.5 + DOWN*2, atom_center + LEFT*0.5 + DOWN*2, color=WHITE)
        lbl1_target = MathTex("|1\\rangle").next_to(g1_target, DOWN)
        
        g2_target = Line(atom_center + RIGHT*0.5 + DOWN*1.8, atom_center + RIGHT*1.5 + DOWN*1.8, color=WHITE)
        lbl2 = MathTex("|2\\rangle").next_to(g2_target, DOWN)

        control_arrow = DoubleArrow(g2_target.get_center(), e3_solid.get_center(), color=BLUE, buff=0.1, stroke_width=6)
        control_lbl = Text("Control", color=BLUE, font_size=18).next_to(control_arrow, RIGHT, buff=0.1)

        split_gap = 0.6
        e3_high = DashedLine(atom_center + LEFT*1 + UP*(1.5+split_gap), atom_center + RIGHT*1 + UP*(1.5+split_gap), color=BLUE_A)
        e3_low  = DashedLine(atom_center + LEFT*1 + UP*(1.5-split_gap), atom_center + RIGHT*1 + UP*(1.5-split_gap), color=BLUE_A)

        # --- ANIMATION PHASE 2 ---
        self.play(Transform(title, title_phase2))

        # 1. Split Ground State
        self.play(
            Transform(g_initial, g1_target),
            Transform(lbl1, lbl1_target),
            GrowFromPoint(g2_target, g_initial.get_center()),
            Write(lbl2),
            probe_arrow.animate.put_start_and_end_on(g1_target.get_center(), e3_solid.get_center()),
            probe_lbl.animate.shift(LEFT*0.5),
            run_time=2
        )

        # 2. Control Laser
        self.play(GrowFromCenter(control_arrow), Write(control_lbl))
        
        # 3. Split Excited State
        self.play(
            e3_solid.animate.set_stroke(opacity=0.25),
            Create(e3_high),
            Create(e3_low),
            lbl3.animate.next_to(e3_high, UP),
            control_arrow.animate.put_start_and_end_on(g2_target.get_center(), atom_center + UP*1.5),
            run_time=2
        )
        
        # Short pause
        gap_text = Text("No Absorption", font_size=16, color=RED).move_to(atom_center + UP*1.5 + LEFT * 2)
        self.play(FadeIn(gap_text))
        self.wait(0.5)
        self.play(FadeOut(gap_text))

        # ==========================================
        #    PHASE 3: DYNAMIC FREQUENCY SCANNING
        # ==========================================

        title_phase3 = Text("Phase 3: EIT Electromagnetically Induced Transparency", font_size=28, color=GREEN).to_edge(UP)
        curve_split = axes.plot(eit_profile, color=GREEN)

        # --- LABEL CHANGE LOGIC ---
        # Create the new Detuning label at the same position as the old Frequency label
        x_lbl_detuning = MathTex(r"\text{Detuning } \Delta", font_size=20).next_to(axes.x_axis, RIGHT)

        # --- STATIC DELTA LABEL ---
        delta_tick = Line(UP*0.1, DOWN*0.1, color=YELLOW).move_to(axes.c2p(2.5, 0))
        delta_label = MathTex(r"\Delta = 0", color=YELLOW, font_size=24).next_to(delta_tick, DOWN)

        # --- DYNAMIC OBJECTS DEFINITION ---
        freq_tracker = ValueTracker(4.0) # Start High

        # Dynamic Arrow
        dynamic_arrow = always_redraw(lambda: Arrow(
            start=g1_target.get_center(), 
            end=atom_center + UP * (1.5 + (freq_tracker.get_value() - 2.5) * energy_scale),
            color=RED, 
            buff=0, 
            stroke_width=4,
            max_tip_length_to_length_ratio=0.15
        ))
        
        # Dynamic Label on Arrow
        dynamic_lbl = always_redraw(lambda: Text(
            "Scanning...", color=RED, font_size=16
        ).next_to(dynamic_arrow, LEFT, buff=0.1))

        # Dynamic Dot on Graph
        dynamic_dot = always_redraw(lambda: Dot(
            point=axes.c2p(freq_tracker.get_value(), eit_profile(freq_tracker.get_value())),
            color=YELLOW,
            radius=0.1
        ))

        # Dynamic Status Text
        def get_status_text():
            f = freq_tracker.get_value()
            if 2.4 <= f <= 2.6: return "At Resonance (Transparency!)"
            else: return "Scanning..."
        
        status_text_obj = always_redraw(lambda: Text(
            get_status_text(), font_size=24, color=WHITE
        ).to_edge(DOWN))

        # --- ANIMATION PHASE 3 ---
        # Update Titles AND Transform Axis Label
        self.play(
            Transform(title, title_phase3),
            Transform(x_lbl, x_lbl_detuning) # <--- THIS IS THE CHANGE
        )

        # 1. Transform Graph & Add Static Delta Label
        self.play(
            Transform(curve_single, curve_split),
            Create(delta_tick),
            Write(delta_label) 
        )

        # 2. Swap Static Probe for Dynamic Probe
        self.remove(probe_arrow, probe_lbl)
        self.add(dynamic_arrow, dynamic_lbl, dynamic_dot, status_text_obj)
        
        # 3. Scan High to Center
        self.play(
            freq_tracker.animate.set_value(2.5),
            run_time=4,
            rate_func=linear
        )
        self.wait(1.0) # Pause at Delta=0 to show alignment

        # 4. Scan Center to Low
        self.play(
            freq_tracker.animate.set_value(1.0),
            run_time=4,
            rate_func=linear
        )

        self.wait(3)
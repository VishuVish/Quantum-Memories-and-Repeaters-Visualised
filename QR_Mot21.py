from manim import *

class QuantumRepeaterSync(Scene):
    def construct(self):
        # -----------------------------------------
        # 1. SETUP & LAYOUT
        # -----------------------------------------
        # FIX: Used r"..." for the string to handle LaTeX backslashes
        # FIX: Changed Text to Tex so the math symbols render correctly
        title = Tex(r"Quantum Repeater: $P_{trans} \propto e^{-L / (2 L_{att})}$", font_size=32, color=GREEN)
        title.to_edge(UP, buff=0.5)
        
        # -----------------------------------------
        # 2. LEFT SIDE: The Graph
        # -----------------------------------------
        axes = Axes(
            x_range=[0, 1000, 500],   
            y_range=[-20, 0, 10],     
            x_length=4.5,
            y_length=3.0,
            axis_config={"color": WHITE, "include_numbers": False},
            tips=False
        )
        axes.move_to(LEFT * 4 + DOWN * 0.2)

        x_label = axes.get_x_axis_label(Text("Distance (km)", font_size=20))
        y_label =  MathTex(r"P_{trans}", font_size=24).next_to(axes.y_axis, UP * 2.5, buff=0.2)
        log_note = Text("(Log Scale)", font_size=16, color=GRAY).next_to(y_label, DOWN, buff=0.1)
        
        # Manual tick labels
        x_nums = VGroup(
            MathTex("0", font_size=20).next_to(axes.c2p(0, -20), DOWN),
            MathTex("500", font_size=20, color=BLUE).next_to(axes.c2p(500, -20), DOWN),
            MathTex("1000", font_size=20).next_to(axes.c2p(1000, -20), DOWN)
        )
        # Used r"" for safety on math strings
        y_nums = VGroup(
            MathTex("1", font_size=20).next_to(axes.c2p(0, 0), LEFT),
            MathTex(r"10^{-10}", font_size=20).next_to(axes.c2p(0, -10), LEFT),
            MathTex(r"10^{-20}", font_size=20).next_to(axes.c2p(0, -20), LEFT)
        )

        # Plot 1: Direct Transmission
        curve_direct = axes.plot(lambda x: -0.02 * x, color=RED, x_range=[0, 1000])
        label_direct = Text("Direct Trans.", font_size=16, color=RED).next_to(curve_direct.get_end(), UP*0.5 + RIGHT*0.2)
        
        # Plot 2: Repeater Assisted
        curve_repeater = axes.plot(lambda x: -0.01 * x, color=GREEN, x_range=[0, 1000])
        label_repeater = Text("w/ Repeater", font_size=16, color=GREEN).next_to(curve_repeater.get_end(), RIGHT)

        # -----------------------------------------
        # 3. RIGHT SIDE: Schematic
        # -----------------------------------------
        start_pos = RIGHT * 0.5 + UP * 0
        mid_pos   = RIGHT * 3.5 + UP * 0
        end_pos   = RIGHT * 6.5 + UP * 0
        
        alice_lbl = Text("Alice", font_size=20).next_to(start_pos, UP)
        bob_lbl   = Text("Bob", font_size=20).next_to(end_pos, UP)
        
        repeater_box = Square(side_length=0.5, color=BLUE, fill_opacity=0.5).move_to(mid_pos)
        # Note: Keep standard string here for \n to work as newline in Text
        repeater_lbl = Text("Repeater\n(500km)", font_size=16, color=BLUE).next_to(repeater_box, UP)
        
        fiber_1 = Line(start_pos, repeater_box.get_left(), color=GRAY)
        fiber_2 = Line(repeater_box.get_right(), end_pos, color=GRAY)
        
        photon = Dot(color=GREEN, radius=0.1)
        photon.move_to(start_pos)
        
        # -----------------------------------------
        # 4. ANIMATION
        # -----------------------------------------
        self.add(title)
        self.play(
            Create(axes), Write(x_label), Write(y_label), 
            Write(x_nums), Write(y_nums), Write(log_note),
            FadeIn(alice_lbl), FadeIn(bob_lbl), FadeIn(repeater_lbl),
            Create(fiber_1), Create(fiber_2), FadeIn(repeater_box)
        )
        
        # Reference Line (Direct)
        direct_group = VGroup(curve_direct, label_direct)
        self.play(Create(curve_direct), Write(label_direct), run_time=1.5)
        self.play(direct_group.animate.set_opacity(0.3))
        self.wait(0.5)

        # Segmented Curves for sync
        curve_seg1 = axes.plot(lambda x: -0.01 * x, color=GREEN, x_range=[0, 500])
        curve_seg2 = axes.plot(lambda x: -0.01 * x, color=GREEN, x_range=[500, 1000])

        self.add(photon)

        # PHASE 1: Alice -> Repeater
        self.play(
            MoveAlongPath(photon, Line(start_pos, repeater_box.get_center())),
            Create(curve_seg1),
            run_time=2,
            rate_func=linear
        )
        
        # PHASE 2: Repeater Operation
        self.play(
            Flash(repeater_box, color=YELLOW, flash_radius=0.5, num_lines=8),
            photon.animate.scale(1.5).set_color(YELLOW),
            run_time=0.5
        )
        self.play(photon.animate.scale(1/1.5).set_color(GREEN), run_time=0.2)
        
        # PHASE 3: Repeater -> Bob
        self.play(
            MoveAlongPath(photon, Line(repeater_box.get_center(), end_pos)),
            Create(curve_seg2),
            run_time=2,
            rate_func=linear
        )
        
        self.play(Write(label_repeater))
        self.wait(2)
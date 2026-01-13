from manim import *

class ExponentialLossPhysics(Scene):
    def construct(self):
        # -----------------------------------------
        # 1. LAYOUT SETUP
        # -----------------------------------------
        title = Text("The Tyranny of Exponential Loss", font_size=42, color=RED)
        title.to_edge(DOWN, buff=0.5)

        # -----------------------------------------
        # 2. LEFT SIDE: The Graph (Graph on Left)
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

        # Graph Labels (Base 10)
        y_label_0 = MathTex("10^0", font_size=24).next_to(axes.c2p(0, 0), LEFT, buff=0.2)
        y_label_10 = MathTex("10^{-10}", font_size=24).next_to(axes.c2p(0, -10), LEFT, buff=0.2)
        y_label_20 = MathTex("10^{-20}", font_size=24).next_to(axes.c2p(0, -20), LEFT, buff=0.2)
        
        x_label_0 = MathTex("0", font_size=24).next_to(axes.c2p(0, -20), DOWN, buff=0.2)
        x_label_1000 = MathTex("1000", font_size=24).next_to(axes.c2p(1000, -20), DOWN, buff=0.2)
        
        x_title = Text("Distance (km)", font_size=20).next_to(axes.x_axis, UP, buff=0.5)
        
        # Y-Axis Title Group (Title + Log Scale Note)
        y_title_text = MathTex(r"P_{trans}", font_size=24)
        log_note = Text("(Log Scale)", font_size=16, color=GRAY)
        
        # Stack them: P_trans on top, Log Scale below it
        y_axis_group = VGroup(y_title_text, log_note).arrange(DOWN, buff=0.1)
        y_axis_group.next_to(axes.y_axis, DOWN, buff=0.2)
        
        graph_line = axes.plot(lambda x: -0.02 * x, color=RED, x_range=[0, 1000])

        # -----------------------------------------
        # 3. RIGHT SIDE: Alice, Bob, Fiber
        # -----------------------------------------
        alice = Text("Alice", font_size=24).move_to(RIGHT * 2.5 + UP * 0.5)
        bob = Text("Bob", font_size=24).move_to(RIGHT * 6.5 + UP * 0.5)
        
        fiber = Line(start=RIGHT * 2.5, end=RIGHT * 6.5, color=BLUE_E, stroke_width=4)
        
        dist_arrow = DoubleArrow(start=RIGHT * 2.5, end=RIGHT * 6.5, buff=0, color=GRAY, stroke_width=2)
        dist_arrow.next_to(fiber, DOWN, buff=0.2)
        
        dist_label = MathTex("L = 1000 \\text{ km}", font_size=20, color=GRAY).next_to(dist_arrow, DOWN, buff=0.1)

        photon = Dot(color=YELLOW, radius=0.08)
        photon.move_to(fiber.get_start())
        
        glow = Dot(color=YELLOW, radius=0.25, fill_opacity=0.4)
        glow.add_updater(lambda m: m.move_to(photon.get_center()))

        # -----------------------------------------
        # 4. CENTER: Equation & Arrow (PHYSICS NOTATION)
        # -----------------------------------------
        equation = MathTex(r"P_{trans} = e^{-\frac{L}{L_{att}}}", font_size=36, color=YELLOW)
        equation.move_to(ORIGIN + UP*0.5)
        
        param_note = MathTex(r"L_{att} \approx 22 \text{ km}", font_size=26, color=GREEN)
        param_note.next_to(equation, UP, buff=0.5)

        center_arrow = Arrow(
            start=equation.get_center() + RIGHT*1.5 + DOWN*0.5,
            end=equation.get_center() + LEFT*1.5 + DOWN*0.5, 
            color=YELLOW, 
            buff=0.1,
        )

        # -----------------------------------------
        # 5. ANIMATION SEQUENCE
        # -----------------------------------------
        self.add(title)

        self.play(
            # Left
            Create(axes), Write(x_title), 
            Write(y_axis_group), # WRITES "P_trans (Log Scale)"
            Write(y_label_0), Write(y_label_10), Write(y_label_20),
            Write(x_label_0), Write(x_label_1000),
            # Right
            FadeIn(alice), FadeIn(bob), Create(fiber), 
            GrowFromCenter(dist_arrow), Write(dist_label),
            # Center
            Write(equation), Write(param_note), GrowArrow(center_arrow)
        )
        self.wait(0.5)

        tracker = ValueTracker(0)
        
        def update_photon(mob):
            val = tracker.get_value()
            progress = val / 1000.0
            mob.move_to(fiber.point_from_proportion(progress))
            mob.set_opacity(1 - progress) 
            
        def update_glow(mob):
            val = tracker.get_value()
            progress = val / 1000.0
            mob.move_to(photon.get_center())
            mob.set_opacity(0.4 * (1 - progress))

        photon.add_updater(update_photon)
        glow.add_updater(update_glow)
        
        self.add(photon, glow)

        self.play(
            Create(graph_line, rate_func=linear),
            tracker.animate.set_value(1000),
            run_time=4,
            rate_func=linear
        )
        
        self.wait(2)

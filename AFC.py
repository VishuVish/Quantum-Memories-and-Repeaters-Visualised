from manim import *
import numpy as np

class AFCEchoSideBySide(Scene):
    def construct(self):
        # ==========================================
        # LAYOUT SETUP
        # ==========================================
        # Create a split screen effect
        # Left: Frequency Domain (The Crystal)
        # Right: Time/Phase Domain (The Physics)
        
        # Title
        title = Text("Atomic Frequency Comb: 2-Level Echo", font_size=36).to_edge(UP)
        self.add(title)

        # ==========================================
        # SECTION 1: THE ENGINEERED COMB (LEFT SIDE)
        # ==========================================
        
        # 1.1 Create Axes
        axes_freq = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 1.5, 1],
            x_length=6,
            y_length=4,
            axis_config={"include_tip": True, "tip_length": 0.2},
        ).to_edge(LEFT, buff=0.5).shift(DOWN*0.5)
        
        freq_label = axes_freq.get_axis_labels(x_label="Frequency", y_label="Absorption")
        
        # 1.2 The Comb Function
        def comb_func(x):
            y = 0.1 # Base absorption
            for i in range(-3, 4): 
                y += np.exp(-20 * (x - i)**2) 
            return y

        comb_graph = axes_freq.plot(comb_func, color=BLUE, x_range=[-3.5, 3.5])
        
        # 1.3 The "Engineered" Indicator
        # We point to the "holes" or the structure to show it's made by humans
        eng_text = Text("Engineered Structure\n(Laser Carved)", color=YELLOW, font_size=24)
        eng_text.next_to(comb_graph, UP + RIGHT, buff=1)
        
        eng_arrow = Arrow(start=eng_text.get_bottom(), end=axes_freq.c2p(0.5, 0.2), color=YELLOW)
        
        # ANIMATION: Show the Crystal
        self.play(Create(axes_freq), Write(freq_label))
        self.play(Create(comb_graph), run_time=2)
        self.play(FadeIn(eng_text), GrowArrow(eng_arrow))
        self.wait(2)
        
        # Remove the indicator to clean up for the physics
        self.play(FadeOut(eng_text), FadeOut(eng_arrow))

        # Show Delta
        delta_arrow = DoubleArrow(
            axes_freq.c2p(0, 1.2), axes_freq.c2p(1, 1.2), buff=0, color=WHITE
        )
        delta_label = MathTex(r"\Delta").next_to(delta_arrow, UP, buff=0.1).scale(0.8)
        self.play(GrowFromCenter(delta_arrow), Write(delta_label))

        # ==========================================
        # SECTION 2: THE PHASE CLOCK (RIGHT SIDE)
        # ==========================================
        
        # 2.1 Setup Circle
        circle = Circle(radius=1.8, color=WHITE, stroke_opacity=0.5)
        circle.to_edge(RIGHT, buff=1.5).shift(DOWN*0.5)
        center_dot = Dot(circle.get_center())
        
        clock_label = Text("Atomic Phase Evolution", font_size=24).next_to(circle, UP)
        
        # 2.2 Create Vectors
        vectors = VGroup()
        indices = range(-3, 4) 
        for i in indices:
            vec = Arrow(
                start=circle.get_center(),
                end=circle.get_top(),
                buff=0,
                color=RED_A if i == 0 else RED_B,
                stroke_width=3
            )
            vectors.add(vec)

        self.play(Create(circle), Create(center_dot), Write(clock_label))
        
        # ==========================================
        # SECTION 3: ABSORPTION & DEPHASING
        # ==========================================
        
        # 3.1 Input Photon (Left Side)
        input_pulse = MathTex(r"\gamma_{in}").move_to(axes_freq.c2p(-5, 0.5)).set_color(YELLOW)
        self.play(
            input_pulse.animate.move_to(axes_freq.c2p(0, 0.5)),
            run_time=1
        )
        self.play(FadeOut(input_pulse), comb_graph.animate.set_color(RED), run_time=0.5)
        
        # 3.2 Vectors appear (Right Side)
        self.play(FadeIn(vectors))
        
        # 3.3 Dephasing Animation
        t = ValueTracker(0)
        
        def update_vectors(mob):
            time = t.get_value()
            for i, vec in zip(indices, mob):
                # Speed = index * Delta * 2 (multiplier for visual speed)
                angle = (np.pi / 2) - (i * 2 * time) 
                new_end = circle.get_center() + np.array([
                    1.8 * np.cos(angle),
                    1.8 * np.sin(angle),
                    0
                ])
                vec.put_start_and_end_on(circle.get_center(), new_end)

        vectors.add_updater(update_vectors)
        
        status_text = Text("Dephasing...", color=RED, font_size=24).next_to(circle, DOWN)
        self.add(status_text)
        
        # Run to 50% (Destructive Interference/Dephasing)
        target_time = np.pi 
        self.play(t.animate.set_value(target_time / 2), run_time=3, rate_func=linear)
        
        status_text.become(Text("Signal Lost (Destructive)", color=GRAY, font_size=24).next_to(circle, DOWN))
        self.wait(1)

        # ==========================================
        # SECTION 4: REPHASING & ECHO
        # ==========================================
        
        status_text.become(Text("Rephasing...", color=YELLOW, font_size=24).next_to(circle, DOWN))
        
        # Run to 100% (Constructive Interference)
        self.play(t.animate.set_value(target_time), run_time=3, rate_func=linear)
        
        # Echo Event
        status_text.become(Text("ECHO!", color=GREEN, font_size=36).next_to(circle, DOWN))
        self.play(Indicate(vectors, color=GREEN, scale_factor=1.2))
        
        # Photon flies out (Left Side)
        echo_pulse = MathTex(r"\gamma_{echo}").set_color(GREEN).move_to(axes_freq.c2p(0, 0.5))
        self.play(
            echo_pulse.animate.move_to(axes_freq.c2p(5, 0.5)),
            run_time=1.5
        )
        
        self.wait(2)
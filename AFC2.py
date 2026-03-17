from manim import *
import numpy as np

class AFCThreeLevel(Scene):
    def construct(self):
        # ==========================================
        # LAYOUT SETUP
        # ==========================================
        title = Text("3-Level AFC: On-Demand Storage", font_size=36).to_edge(UP)
        self.add(title)

        # LEFT SIDE: Lambda Energy System
        # |e> (Excited)
        # |g> (Ground)   |s> (Storage/Spin)
        
        # Coordinates for levels
        g_pos = LEFT * 5 + DOWN * 2
        s_pos = LEFT * 3 + DOWN * 1.5
        e_pos = LEFT * 4 + UP * 1
        
        # Draw Levels
        level_g = Line(start=g_pos + LEFT*0.5, end=g_pos + RIGHT*0.5, color=WHITE)
        level_s = Line(start=s_pos + LEFT*0.5, end=s_pos + RIGHT*0.5, color=WHITE)
        level_e = Line(start=e_pos + LEFT*0.5, end=e_pos + RIGHT*0.5, color=WHITE)
        
        lbl_g = MathTex(r"|g\rangle").next_to(level_g, DOWN)
        lbl_s = MathTex(r"|s\rangle").next_to(level_s, DOWN)
        lbl_e = MathTex(r"|e\rangle").next_to(level_e, UP)
        
        lambda_group = VGroup(level_g, level_s, level_e, lbl_g, lbl_s, lbl_e)
        self.play(Create(lambda_group))
        
        # RIGHT SIDE: Phase Clock
        circle = Circle(radius=1.8, color=WHITE, stroke_opacity=0.5).to_edge(RIGHT, buff=1.5).shift(DOWN*0.5)
        center_dot = Dot(circle.get_center())
        clock_label = Text("Phase Evolution", font_size=24).next_to(circle, UP)
        
        vectors = VGroup()
        indices = range(-3, 4)
        for i in indices:
            vec = Arrow(start=circle.get_center(), end=circle.get_top(), buff=0, color=RED, stroke_width=3)
            vectors.add(vec)
            
        self.play(Create(circle), Create(center_dot), Write(clock_label), FadeIn(vectors))

       # ==========================================
        # 1. INPUT PHOTON (DETAILED VISUALIZATION)
        # ==========================================
        
        # A. Show the Comb Structure on |e>
        # Create 5 small lines "teeth" on top of the excited state
        teeth = VGroup()
        for i in range(-2, 3):
            tooth = Line(start=UP*0, end=UP*0.2, color=WHITE).move_to(e_pos + RIGHT*0.2*i + UP*0.2)
            teeth.add(tooth)
        
        comb_label = Text("Frequency Comb", font_size=20, color=WHITE).next_to(teeth, RIGHT, buff=0.1)
        
        self.play(Create(teeth), FadeIn(comb_label))
        self.wait(0.5)

        # B. Create the Broadband Pulse (Wave Packet)
        # We simulate a pulse moving from bottom to top
        pulse_path = Line(start=g_pos + UP*0.5, end=e_pos + DOWN*0.2)
        
        # Create a wave shape
        wave = FunctionGraph(
            lambda x: 0.2 * np.sin(10 * x) * np.exp(-3 * x**2), 
            x_range=[-2, 2], 
            color=YELLOW
        ).rotate(PI/2).scale(0.5).move_to(g_pos + UP*1)
        
        pulse_label = Text("Broadband Pulse", font_size=20, color=YELLOW).next_to(wave, LEFT)
        
        self.play(FadeIn(wave), FadeIn(pulse_label))
        
        # C. Animate Pulse Absorption
        # Move wave to the comb
        self.play(
            wave.animate.move_to(e_pos),
            pulse_label.animate.next_to(e_pos, LEFT),
            run_time=1.5
        )
        
        # D. Absorption Effect
        # Flash the teeth YELLOW to show they absorbed specific frequencies
        self.play(
            teeth.animate.set_color(YELLOW),
            FadeOut(wave), # Pulse is absorbed
            FadeOut(pulse_label),
            FadeOut(comb_label),
            run_time=0.5
        )
        
        # Clean up visualization for the next steps
        # Fade out teeth, replace with the "Pop Dot" for the rest of the animation
        pop_dot = Dot(color=YELLOW).move_to(level_e.get_center())
        self.play(Transform(teeth, pop_dot)) # The comb becomes the population
        
        # (Proceed to Step 2: Dephasing...)
        
        # 2. DEPHASING STARTS
        t = ValueTracker(0)
        
        # Updater for vectors (Standard dephasing)
        def update_vectors(mob):
            time = t.get_value()
            for i, vec in zip(indices, mob):
                angle = (np.pi / 2) - (i * 2 * time) 
                new_end = circle.get_center() + np.array([1.8 * np.cos(angle), 1.8 * np.sin(angle), 0])
                vec.put_start_and_end_on(circle.get_center(), new_end)
        
        vectors.add_updater(update_vectors)
        
        # Run briefly (Phase 1)
        self.play(t.animate.set_value(1.0), run_time=1.5, rate_func=linear)
        
        # 3. WRITE PULSE (Control Laser 1)
        # Stop the updater! (Freeze time)
        vectors.remove_updater(update_vectors)
        current_time = t.get_value() # Save where we stopped
        
        # Visual: Strong Red Pulse connecting |e> and |s>
        control_arrow = DoubleArrow(start=e_pos + DOWN*0.2, end=s_pos + UP*0.2, color=RED, buff=0)
        pulse_text = Text("WRITE PULSE", color=RED, font_size=24).next_to(control_arrow, RIGHT)
        
        self.play(GrowArrow(control_arrow), Write(pulse_text), run_time=0.5)
        
        # Move population dot to |s> (The Shelf)
        self.play(pop_dot.animate.move_to(level_s.get_center()), run_time=0.5)
        
        # "Freeze" visual on the clock (Turn vectors Grey to show storage)
        self.play(vectors.animate.set_color(GRAY))
        
        # Remove pulse
        self.play(FadeOut(control_arrow), FadeOut(pulse_text))
        
        # 4. STORAGE (The Wait)
        # Add a label showing that the phase is locked
        lock_text = MathTex(r"\frac{d\phi}{dt} = 0").next_to(circle, DOWN)
        wait_text = Text("STORING... (Spin Wave)", font_size=36, color=BLUE).move_to(LEFT*4 + UP*0)
        
        self.play(FadeIn(wait_text), Write(lock_text))
        self.wait(2) 
        self.play(FadeOut(wait_text), FadeOut(lock_text))

        
        # 5. READ PULSE (Control Laser 2)
        # Visual: Strong Red Pulse connecting |s> and |e>
        control_arrow_2 = DoubleArrow(start=s_pos + UP*0.2, end=e_pos + DOWN*0.2, color=RED, buff=0)
        pulse_text_2 = Text("READ PULSE", color=RED, font_size=24).next_to(control_arrow_2, RIGHT)
        
        self.play(GrowArrow(control_arrow_2), Write(pulse_text_2), run_time=0.5)
        
        # Move population back to |e>
        self.play(pop_dot.animate.move_to(level_e.get_center()), run_time=0.5)
        
        # Unfreeze clock (Turn vectors Red again)
        self.play(vectors.animate.set_color(RED))
        
        # Remove pulse
        self.play(FadeOut(control_arrow_2), FadeOut(pulse_text_2))
        
        # 6. REPHASING RESUMES
        # Re-attach updater, starting from where we left off
        vectors.add_updater(update_vectors)
        
        # Calculate target time for rephasing (Pi)
        target_time = np.pi
        
        # Animate the rest of the way
        self.play(t.animate.set_value(target_time), run_time=1.5, rate_func=linear)
        
        # 7. ECHO
        vectors.remove_updater(update_vectors) # Stop at perfect alignment
        
        echo_text = Text("ECHO ON DEMAND!", color=GREEN, font_size=36).next_to(circle, DOWN)
        self.play(Indicate(vectors, color=GREEN, scale_factor=1.2), Write(echo_text))
        
        # Photon leaves |e> to |g>
        emit_arrow = Arrow(start=e_pos + DOWN*0.2, end=g_pos + UP*0.2, color=GREEN, buff=0)
        self.play(GrowArrow(emit_arrow), run_time=0.5)
        self.play(FadeOut(pop_dot), FadeOut(emit_arrow))
        
        self.wait(2)
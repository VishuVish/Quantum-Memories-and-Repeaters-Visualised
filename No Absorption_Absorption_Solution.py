from manim import *

class Part1_Transparency(Scene):
    def construct(self):
        # 1. SETUP
        # Crystal (Glass-like)
        crystal = Rectangle(height=2, width=5, color=WHITE, fill_opacity=0.1)
        title = Text("No Interaction Case", font_size=36).next_to(crystal,UP*2)
        label_od = Text("Glass (OD ≈ 0)", font_size=24, color=WHITE).next_to(crystal, DOWN)
        
        # The Photon
        photon = Dot(color=YELLOW, radius=0.15)
        photon.move_to(LEFT * 6) # Start off-screen left

        # Add static elements
        self.add(title, crystal, label_od)

        # 2. ANIMATION
        # Photon flies straight through without slowing down
        self.play(
            photon.animate.move_to(RIGHT * 6),
            run_time=2,
            rate_func=linear
        )
        self.wait(0.5)

from manim import *

class Part2_Absorption(Scene):
    def construct(self):
        # 1. SETUP
        crystal = Rectangle(height=2, width=5, color=WHITE, fill_opacity=0.2)
        title = Text("Resonant Absorption Case", font_size=36, color=WHITE).next_to(crystal,UP*2)
        label_od = MathTex(r"\text{Resonant Medium } (OD \gg 1)", color=WHITE, font_size=28).next_to(crystal, DOWN)
        
        # The Photon
        photon = Dot(color=YELLOW, radius=0.15).move_to(LEFT * 6)

        self.add(title, crystal, label_od)

        # 2. ANIMATION
        # Move to center
        self.play(
            photon.animate.move_to(crystal.get_center()),
            run_time=1.0,
            rate_func=linear
        )
        
        # 3. THE "DEATH" OF THE PHOTON
        # Flash effect to show energy loss
        flash = Flash(crystal.get_center(), color=RED, line_length=0.5, num_lines=12)
        loss_text = Text("Absorption Loss", font_size=30, color=RED).next_to(crystal, RIGHT)

        self.play(
            FadeOut(photon),      # Photon disappears
            flash,                # Explosion effect
            crystal.animate.set_fill(RED, opacity=0.6), # Crystal flashes bright red
            Write(loss_text),
            run_time=0.5
        )
        
        # Cool down slightly
        self.play(crystal.animate.set_fill(RED, opacity=0.2)) 
        self.wait(1)

from manim import *

class Part3_Solution(Scene):
    def construct(self):
        # 1. SETUP
        # Crystal (Blue to indicate "Cool/Coherent")
        crystal = Rectangle(height=2, width=5, color=WHITE, fill_opacity=0.2)
        title = Text("Solution(s) (EIT / AFC)", font_size=36, color=WHITE).next_to(crystal, UP*2)
        label_od = MathTex(r"\chi(\omega) \text{ Engineered}", color=WHITE, font_size=28).next_to(crystal, DOWN)
        
        # The Photon
        photon = Dot(color=YELLOW, radius=0.15).move_to(LEFT * 6)
        
        self.add(title, crystal, label_od)

        # 2. ANIMATION: ENTERING
        # Move to the edge of the crystal fast
        self.play(
            photon.animate.move_to(crystal.get_left()),
            run_time=0.5,
            rate_func=linear
        )
        
        # 3. ANIMATION: SLOW LIGHT EFFECT
        # Move to center SLOWLY (showing massive dispersion/group velocity reduction)
        self.play(
            photon.animate.move_to(crystal.get_center()),
            run_time=2.0,
            rate_func=rush_into # Decelerates as it enters
        )
        
        # 4. MAPPING TO SPIN WAVE
        # Create the stored state representation (a glowing ring)
        spin_wave = Circle(radius=0.4, color=BLUE_E, fill_opacity=0.5).move_to(crystal.get_center())
        text_stored = Text("Coherent Mapping", font_size=30, color=BLUE).next_to(crystal, RIGHT)
        
        self.play(
            Transform(photon, spin_wave),  # Photon morphs into matter
            Write(text_stored),
            crystal.animate.set_fill(BLUE, opacity=0.4), # Crystal glows slightly to show storage
            run_time=1.0
        )
        
        # Pulse to show it's alive (preserving phase)
        self.play(
            photon.animate.scale(1.2), # 'photon' is now the spin_wave object due to Transform
            rate_func=there_and_back,
            run_time=1.0
        )
        self.wait(1)
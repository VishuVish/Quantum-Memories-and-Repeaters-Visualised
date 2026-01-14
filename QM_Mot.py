from manim import *

# ============================================

# SCENE 1: Quantum Repeater WITHOUT Quantum Memory

# ============================================

class QR_Without_Memory(Scene):
    def construct(self):
        # --- Title ---
        title = Text("Quantum Repeater: Without Memory", font_size=32, color=RED)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        
        # --- Setup: 3 Nodes ---
        node_a = VGroup(
            Circle(radius=0.5, color=BLUE, fill_opacity=0.3),
            Text("A", font_size=28)
        ).move_to(LEFT * 4)
        
        node_r = VGroup(
            Circle(radius=0.5, color=GREEN, fill_opacity=0.3),
            Text("R", font_size=28)
        ).move_to(ORIGIN)
        
        node_b = VGroup(
            Circle(radius=0.5, color=BLUE, fill_opacity=0.3),
            Text("B", font_size=28)
        ).move_to(RIGHT * 4)
        
        # Links (gray = inactive)
        link_ar = Line(LEFT * 3.4, LEFT * 0.6, color=GRAY, stroke_width=4)
        link_rb = Line(RIGHT * 0.6, RIGHT * 3.4, color=GRAY, stroke_width=4)
        
        # Labels for links
        label_ar = Text("Link 1", font_size=20, color=GRAY).next_to(link_ar, UP, buff=0.1)
        label_rb = Text("Link 2", font_size=20, color=GRAY).next_to(link_rb, UP, buff=0.1)
        
        self.play(
            FadeIn(node_a), FadeIn(node_r), FadeIn(node_b),
            Create(link_ar), Create(link_rb),
            Write(label_ar), Write(label_rb)
        )
        self.wait(0.5)
        
        # --- Subtitle: Requirement ---
        requirement = Text("Both links must succeed simultaneously!", font_size=24, color=YELLOW)
        requirement.next_to(title, DOWN, buff=0.3)
        self.play(Write(requirement))
        self.wait(0.5)
        
        # --- Attempt Counter ---
        attempt_text = Text("Attempt: ", font_size=24).to_corner(DL, buff=0.5)
        attempt_num = Integer(1).next_to(attempt_text, RIGHT)
        attempt_group = VGroup(attempt_text, attempt_num)
        self.play(Write(attempt_group))
        
        # --- Define success/failure patterns ---
        # Format: (link1_success, link2_success)
        attempts = [
            (True, False),   # Attempt 1: Link 1 succeeds, Link 2 fails
            (False, True),   # Attempt 2: Link 1 fails, Link 2 succeeds
            (False, False),  # Attempt 3: Both fail
            (True, False),   # Attempt 4: Link 1 succeeds, Link 2 fails
            (True, True),    # Attempt 5: Both succeed!
        ]
        
        status_text = None
        
        for i, (ar_success, rb_success) in enumerate(attempts):
            # Update attempt counter
            if i > 0:
                self.play(attempt_num.animate.set_value(i + 1), run_time=0.3)
            
            # Flash both links simultaneously
            ar_color = GREEN if ar_success else RED
            rb_color = GREEN if rb_success else RED
            
            ar_flash = Line(LEFT * 3.4, LEFT * 0.6, color=ar_color, stroke_width=8)
            rb_flash = Line(RIGHT * 0.6, RIGHT * 3.4, color=rb_color, stroke_width=8)
            
            # Show link results
            ar_result = Text("✓" if ar_success else "✗", font_size=28, color=ar_color)
            ar_result.next_to(link_ar, DOWN, buff=0.1)
            rb_result = Text("✓" if rb_success else "✗", font_size=28, color=rb_color)
            rb_result.next_to(link_rb, DOWN, buff=0.1)
            
            self.play(
                Create(ar_flash),
                Create(rb_flash),
                FadeIn(ar_result),
                FadeIn(rb_result),
                run_time=0.5
            )
            
            # Check if both succeeded
            if ar_success and rb_success:
                # SUCCESS!
                if status_text:
                    self.play(FadeOut(status_text))
                
                status_text = Text("✓ Success!", font_size=36, color=GREEN)
                status_text.to_edge(DOWN, buff=0.8)
                self.play(Write(status_text))
                self.wait(1)
                
                # Show final entanglement A-B
                final_link = ArcBetweenPoints(
                    LEFT * 4, RIGHT * 4,
                    angle=-PI/5,
                    color=PURPLE,
                    stroke_width=6
                )
                final_label = Text("A-B Entangled!", font_size=24, color=PURPLE)
                final_label.next_to(final_link, UP, buff=0.3)
                
                self.play(
                    FadeOut(ar_flash), FadeOut(rb_flash),
                    FadeOut(ar_result), FadeOut(rb_result),
                    Create(final_link),
                    Write(final_label),
                    run_time=1
                )
                break
            else:
                # FAILURE - must retry
                if status_text:
                    self.play(FadeOut(status_text), run_time=0.2)
                
                status_text = Text("✗ Retry!", font_size=36, color=RED)
                status_text.to_edge(DOWN, buff=0.8)
                self.play(Write(status_text), run_time=0.3)
                
                self.wait(0.5)
                
                # Reset - fade out the flashes
                self.play(
                    FadeOut(ar_flash), FadeOut(rb_flash),
                    FadeOut(ar_result), FadeOut(rb_result),
                    run_time=0.4
                )
        
        self.wait(2)


# ============================================

# SCENE 2: Quantum Repeater WITH Quantum Memory

# ============================================

class QR_With_Memory(Scene):
    def construct(self):
        # --- Title ---
        title = Text("Quantum Repeater: With Memory", font_size=32, color=GREEN)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        
        # --- Setup: 3 Nodes ---
        node_a = VGroup(
            Circle(radius=0.5, color=BLUE, fill_opacity=0.3),
            Text("A", font_size=28)
        ).move_to(LEFT * 4)
        
        node_r_circle = Circle(radius=0.5, color=GREEN, fill_opacity=0.3)
        node_r_text = Text("R", font_size=28)
        node_r = VGroup(node_r_circle, node_r_text).move_to(ORIGIN)
        
        node_b = VGroup(
            Circle(radius=0.5, color=BLUE, fill_opacity=0.3),
            Text("B", font_size=28)
        ).move_to(RIGHT * 4)
        
        # Memory at Repeater
        memory_box = RoundedRectangle(
            width=0.8, height=0.4, 
            corner_radius=0.1,
            color=YELLOW, 
            fill_opacity=0.2,
            stroke_width=2
        ).next_to(node_r, DOWN, buff=0.15)
        memory_label = Text("Memory", font_size=14, color=YELLOW).next_to(memory_box, DOWN, buff=0.05)
        
        # Links (gray = inactive)
        link_ar = Line(LEFT * 3.4, LEFT * 0.6, color=GRAY, stroke_width=4)
        link_rb = Line(RIGHT * 0.6, RIGHT * 3.4, color=GRAY, stroke_width=4)
        
        # Labels for links
        label_ar = Text("Link 1", font_size=20, color=GRAY).next_to(link_ar, UP, buff=0.1)
        label_rb = Text("Link 2", font_size=20, color=GRAY).next_to(link_rb, UP, buff=0.1)
        
        self.play(
            FadeIn(node_a), FadeIn(node_r), FadeIn(node_b),
            Create(link_ar), Create(link_rb),
            Write(label_ar), Write(label_rb),
            FadeIn(memory_box), Write(memory_label)
        )
        self.wait(0.5)
        
        # --- Subtitle: Key Advantage ---
        advantage = Text("Store success, retry independently!", font_size=24, color=YELLOW)
        advantage.next_to(title, DOWN, buff=0.3)
        self.play(Write(advantage))
        self.wait(0.5)
        
        # --- Phase 1: Establish Link 1 (A-R) ---
        phase1_text = Text("Step 1: Establish Link 1", font_size=22, color=WHITE)
        phase1_text.to_corner(DL, buff=0.5)
        self.play(Write(phase1_text))
        
        # Attempt Link 1 - fail first
        ar_flash_fail = Line(LEFT * 3.4, LEFT * 0.6, color=RED, stroke_width=8)
        ar_result_fail = Text("✗", font_size=28, color=RED).next_to(link_ar, DOWN, buff=0.1)
        
        self.play(Create(ar_flash_fail), FadeIn(ar_result_fail), run_time=0.5)
        
        retry1_text = Text("Retry...", font_size=24, color=RED).to_edge(DOWN, buff=0.8)
        self.play(Write(retry1_text), run_time=0.3)
        self.wait(0.3)
        self.play(FadeOut(ar_flash_fail), FadeOut(ar_result_fail), FadeOut(retry1_text), run_time=0.3)
        
        # Attempt Link 1 - succeed
        ar_flash_success = Line(LEFT * 3.4, LEFT * 0.6, color=GREEN, stroke_width=8)
        ar_result_success = Text("✓", font_size=28, color=GREEN).next_to(link_ar, DOWN, buff=0.1)
        
        self.play(Create(ar_flash_success), FadeIn(ar_result_success), run_time=0.5)
        
        # Store in memory!
        store_text = Text("✓ Stored in Memory!", font_size=24, color=GREEN).to_edge(DOWN, buff=0.8)
        self.play(
            Write(store_text),
            memory_box.animate.set_fill(GREEN, opacity=0.6),
            run_time=0.5
        )
        
        # Keep Link 1 visible (stored state)
        ar_stored = Line(LEFT * 3.4, LEFT * 0.6, color=GREEN, stroke_width=6)
        self.play(
            FadeOut(ar_flash_success),
            Create(ar_stored),
            FadeOut(ar_result_success),
            FadeOut(store_text),
            run_time=0.4
        )
        
        # --- Phase 2: Establish Link 2 (R-B) independently ---
        self.play(FadeOut(phase1_text))
        phase2_text = Text("Step 2: Establish Link 2 (independently)", font_size=22, color=WHITE)
        phase2_text.to_corner(DL, buff=0.5)
        self.play(Write(phase2_text))
        
        # Attempt Link 2 - fail first
        rb_flash_fail = Line(RIGHT * 0.6, RIGHT * 3.4, color=RED, stroke_width=8)
        rb_result_fail = Text("✗", font_size=28, color=RED).next_to(link_rb, DOWN, buff=0.1)
        
        self.play(Create(rb_flash_fail), FadeIn(rb_result_fail), run_time=0.5)
        
        # Key point: Link 1 still stored!
        retry2_text = Text("Retry... (Link 1 still stored!)", font_size=24, color=YELLOW).to_edge(DOWN, buff=0.8)
        
        # Pulse memory to show it's still holding
        self.play(
            Write(retry2_text),
            memory_box.animate.set_stroke(width=4),
            run_time=0.4
        )
        self.play(memory_box.animate.set_stroke(width=2), run_time=0.2)
        
        self.play(FadeOut(rb_flash_fail), FadeOut(rb_result_fail), FadeOut(retry2_text), run_time=0.3)
        
        # Attempt Link 2 - fail again
        rb_flash_fail2 = Line(RIGHT * 0.6, RIGHT * 3.4, color=RED, stroke_width=8)
        rb_result_fail2 = Text("✗", font_size=28, color=RED).next_to(link_rb, DOWN, buff=0.1)
        
        self.play(Create(rb_flash_fail2), FadeIn(rb_result_fail2), run_time=0.5)
        
        retry3_text = Text("Retry...", font_size=24, color=RED).to_edge(DOWN, buff=0.8)
        self.play(Write(retry3_text), run_time=0.3)
        self.play(FadeOut(rb_flash_fail2), FadeOut(rb_result_fail2), FadeOut(retry3_text), run_time=0.3)
        
        # Attempt Link 2 - succeed!
        rb_flash_success = Line(RIGHT * 0.6, RIGHT * 3.4, color=GREEN, stroke_width=8)
        rb_result_success = Text("✓", font_size=28, color=GREEN).next_to(link_rb, DOWN, buff=0.1)
        
        self.play(Create(rb_flash_success), FadeIn(rb_result_success), run_time=0.5)
        
        success2_text = Text("✓ Both links ready!", font_size=24, color=GREEN).to_edge(DOWN, buff=0.8)
        self.play(Write(success2_text))
        self.wait(0.5)
        
        # --- Phase 3: Entanglement Swapping ---
        self.play(FadeOut(phase2_text), FadeOut(success2_text))
        phase3_text = Text("Step 3: Entanglement Swapping", font_size=22, color=WHITE)
        phase3_text.to_corner(DL, buff=0.5)
        self.play(Write(phase3_text))
        
        # Flash at repeater (BSM)
        bsm_flash = Circle(radius=0.7, color=YELLOW, fill_opacity=0.5).move_to(ORIGIN)
        bsm_text = Text("BSM", font_size=20, color=BLACK).move_to(ORIGIN)
        
        self.play(
            FadeIn(bsm_flash, scale=0.5),
            FadeIn(bsm_text),
            run_time=0.5
        )
        self.play(
            FadeOut(bsm_flash),
            FadeOut(bsm_text),
            FadeOut(ar_stored),
            FadeOut(rb_flash_success),
            FadeOut(rb_result_success),
            memory_box.animate.set_fill(YELLOW, opacity=0.2),
            run_time=0.5
        )
        
        # Show final entanglement A-B
        final_link = ArcBetweenPoints(
            LEFT * 4, RIGHT * 4,
            angle=-PI/5,
            color=PURPLE,
            stroke_width=6
        )
        final_label = Text("A-B Entangled!", font_size=28, color=PURPLE)
        final_label.next_to(final_link, UP, buff=0.3)
        
        success_final = Text("✓ Success!", font_size=36, color=GREEN).to_edge(DOWN, buff=0.8)
        
        self.play(
            Create(final_link),
            Write(final_label),
            Write(success_final),
            FadeOut(phase3_text),
            run_time=1
        )
        
        self.wait(2)
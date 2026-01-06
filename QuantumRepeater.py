from manim import *

# -----------------------------------------
# HELPER: Define Styles and Positions once
# -----------------------------------------
def get_base_layout():
    # Positions
    pos_a = LEFT * 5 + UP * 1.5
    pos_b = LEFT * 1.5 + UP * 1.5
    pos_c = RIGHT * 1.5 + UP * 1.5
    pos_d = RIGHT * 5 + UP * 1.5
    
    # Node Configuration
    box_config = {"color": BLUE, "fill_opacity": 0.2, "side_length": 1.2}
    
    # Node A
    node_a = VGroup(Square(**box_config), Text("A").scale(0.8)).move_to(pos_a)
    
    # Node B (with memory slots)
    box_b = Square(**box_config).move_to(pos_b)
    mem_b_l = Square(side_length=0.4, color=WHITE).move_to(pos_b + LEFT*0.3)
    mem_b_r = Square(side_length=0.4, color=WHITE).move_to(pos_b + RIGHT*0.3)
    label_b = Text("B").scale(0.8).next_to(box_b, UP)
    node_b = VGroup(box_b, mem_b_l, mem_b_r, label_b)
    
    # Node C (with memory slots)
    box_c = Square(**box_config).move_to(pos_c)
    mem_c_l = Square(side_length=0.4, color=WHITE).move_to(pos_c + LEFT*0.3)
    mem_c_r = Square(side_length=0.4, color=WHITE).move_to(pos_c + RIGHT*0.3)
    label_c = Text("C").scale(0.8).next_to(box_c, UP)
    node_c = VGroup(box_c, mem_c_l, mem_c_r, label_c)
    
    # Node D
    node_d = VGroup(Square(**box_config), Text("D").scale(0.8)).move_to(pos_d)
    
    # Return dictionary of points and objects for easy access
    return {
        "pos": [pos_a, pos_b, pos_c, pos_d],
        "nodes": [node_a, node_b, node_c, node_d]
    }

# -----------------------------------------
# IMAGE 1: Entangle & Store
# -----------------------------------------
class Case1_Entangle(Scene):
    def construct(self):
        layout = get_base_layout()
        pos = layout["pos"]
        nodes = layout["nodes"]
        
        # Add Nodes
        self.add(*nodes)
        
        # Title
        title = Text("1. Entangle & Store", font_size=36).to_corner(UL)
        self.add(title)

        # Links (Short Range)
        link_ab = Line(pos[0] + RIGHT*0.6, pos[1] + LEFT*0.6, color=TEAL)
        link_bc = Line(pos[1] + RIGHT*0.6, pos[2] + LEFT*0.6, color=TEAL)
        link_cd = Line(pos[2] + RIGHT*0.6, pos[3] + LEFT*0.6, color=TEAL)
        self.add(link_ab, link_bc, link_cd)
        
        nodes_group = VGroup(*nodes)

        # Math
        math = MathTex(
            r"|\Psi_{init}\rangle = |\Phi^+\rangle_{A,B_L} \otimes |\Phi^+\rangle_{B_R,C_L} \otimes |\Phi^+\rangle_{C_R,D}",
            font_size=46
        ).next_to(nodes_group, DOWN, buff=1)
        self.add(math)

# -----------------------------------------
# IMAGE 2: Bell State Measurement at B
# -----------------------------------------
class Case2_SwapB(Scene):
    def construct(self):
        layout = get_base_layout()
        pos = layout["pos"]
        nodes = layout["nodes"]
        
        # Modify State: B is measured (Gray out B, Highlight Red)
        nodes[1].set_opacity(0.3) 
        highlight_b = SurroundingRectangle(nodes[1], color=RED, buff=0.1)
        
        self.add(*nodes, highlight_b)
        
        # Title
        title = Text("2. Bell State Measurement at B (Swap)", font_size=36).to_corner(UL)
        self.add(title)

        # Links: AB and BC are gone. AC is created.
        # Still show CD
        link_cd = Line(pos[2] + RIGHT*0.6, pos[3] + LEFT*0.6, color=TEAL)
        link_ac = ArcBetweenPoints(pos[0] + RIGHT*0.6, pos[2] + LEFT*0.6, angle=-PI/4, color=TEAL)
        
        self.add(link_cd, link_ac)
        
        nodes_group = VGroup(*nodes)
        # Math
        math = MathTex(
            r"\text{Measure } B \rightarrow |\Phi^+\rangle_{A,C_L} \otimes |\Phi^+\rangle_{C_R,D}",
            font_size=46
        ).next_to(nodes_group, DOWN, buff=1)
        self.add(math)

# -----------------------------------------
# IMAGE 3: Final Measurement at C
# -----------------------------------------
class Case3_Final(Scene):
    def construct(self):
        layout = get_base_layout()
        pos = layout["pos"]
        nodes = layout["nodes"]
        
        # Modify State: B and C are consumed
        nodes[1].set_opacity(0.3)
        nodes[2].set_opacity(0.3)
        
        # Highlight A and D (Success)
        highlight_a = SurroundingRectangle(nodes[0], color=PURPLE, buff=0.1)
        highlight_d = SurroundingRectangle(nodes[3], color=PURPLE, buff=0.1)
        
        self.add(*nodes, highlight_a, highlight_d)

        # Title
        title = Text("3. Final Measurement at C", font_size=36).to_corner(UL)
        self.add(title)
        
        # Links: Only AD exists now
        link_ad = ArcBetweenPoints(pos[0] + RIGHT*0.6, pos[3] + LEFT*0.6, angle=-PI/3, color=PURPLE)
        self.add(link_ad)
        
        nodes_group = VGroup(*nodes)
        # Math
        math = MathTex(
            r"|\Psi_{final}\rangle_{AD} = \frac{1}{\sqrt{2}} (|00\rangle_{AD} + |11\rangle_{AD})",
            font_size=46
        ).next_to(nodes_group, DOWN, buff=1)
        self.add(math)
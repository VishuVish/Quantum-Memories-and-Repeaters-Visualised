# Quantum-Memories-and-Repeaters-Visualised 

This repository contains a collection of **Manim (Mathematical Animation Engine)** Python scripts used to visualize complex quantum optical phenomena. 

These animations were developed to illustrate the physics behind **Quantum Memories** (EIT, AFC) and **Quantum Repeater protocols** for a Master's thesis presentation on Quantum Networks.

## 📦 Requirements

* **Python 3.10+**
* **Manim Community Edition**
* **NumPy**

🚀 Quick Start
To render a specific scene, run the following command in your terminal:

manim -pql <filename.py> <SceneName>

-p: Plays the video immediately after rendering.
-ql: Renders in Low Quality (fast for testing).
Use -qh for High Quality (1080p) output.

🛠️ Usage Examples
To render the full EIT storage process:
manim -qh EIT_to_QuantumMemory.py EITMemoryLambda

To render the Atomic Frequency Comb echo:
manim -qh AFC.py AFCEchoSideBySide

To render the Entanglement Swapping Network (Step 2):
manim -qh QuantumRepeater.py Case2_SwapB

This code is provided for educational and academic presentation purposes. Feel free to modify the parameters (Rabi frequencies, decay rates, colors) to fit your specific presentation theme.

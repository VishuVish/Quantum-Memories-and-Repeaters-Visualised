# Quantum Memories and Repeaters — Visualised

A collection of **Manim** animations built to explain the physics behind 
quantum memories and quantum repeater protocols — developed as part of an 
advanced seminar presentation at the **Abbe School of Photonics, FSU Jena**.

These animations cover electromagnetically induced transparency (EIT), 
atomic frequency combs (AFC), and quantum repeater architectures — 
visualising concepts that are typically buried in dense mathematical formalism.

---

## Animation Previews

### Why Do We Need Quantum Memory?
https://github.com/VishuVish/Quantum-Memories-and-Repeaters-Visualised/blob/main/WhyQuantumMemory.mp4

### EIT — Electromagnetically Induced Transparency
https://github.com/VishuVish/Quantum-Memories-and-Repeaters-Visualised/blob/main/EIT_Visualized.mp4

### EIT Slope Variation
https://github.com/VishuVish/Quantum-Memories-and-Repeaters-Visualised/blob/main/EITSlopeVariation.mp4

### AFC — Atomic Frequency Comb (Three-Level System)
https://github.com/VishuVish/Quantum-Memories-and-Repeaters-Visualised/blob/main/AFCThreeLevel.mp4

### AFC Echo Side-by-Side Comparison
https://github.com/VishuVish/Quantum-Memories-and-Repeaters-Visualised/blob/main/AFCEchoSideBySide.mp4

### Quantum Repeater — With Memory
https://github.com/VishuVish/Quantum-Memories-and-Repeaters-Visualised/blob/main/QR_With_Memory.mp4

### Quantum Repeater — Without Memory
https://github.com/VishuVish/Quantum-Memories-and-Repeaters-Visualised/blob/main/QR_Without_Memory.mp4

---

## Seminar Presentation

The full seminar slides accompanying these animations are available here:
[Quantum Memories and Quantum Repeaters.pdf](https://github.com/VishuVish/Quantum-Memories-and-Repeaters-Visualised/blob/main/Quantum%20Memories%20and%20Quantum%20Repeaters.pdf)

---

## Repository Structure

| File | Description |
|---|---|
| `EIT.py` | Basic EIT transparency window animation |
| `EIT_Slope.py` | Group velocity and slope variation |
| `EIT_to_KKRel.py` | EIT to Kramers-Kronig relations |
| `EIT_to_QuantumMemory.py` | EIT as a quantum memory mechanism |
| `AFC.py` / `AFC2.py` | Atomic frequency comb protocols |
| `QM_Mot.py` | Quantum memory motivation |
| `QR_Motivation.py` / `QR_Mot21.py` | Quantum repeater motivation |
| `QuantumRepeater.py` | Full repeater protocol animation |

---

## Requirements

- Python 3.10+
- Manim Community Edition
- NumPy

##  Quick Start
```bash
manim -pql <filename.py> <SceneName>
```

---

*Developed by Vishnuthirtha Sandur Huliraj — Master's student in Quantum 
Sciences and Technology, Abbe School of Photonics, FSU Jena.*


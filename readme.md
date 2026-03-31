# 🧬 RTX Neural Physics Threads

A real-time computer vision application that bridges the gap between skeletal tracking and procedural physics. **RTX Neural Physics Threads** uses MediaPipe's hand landmarks to anchor dynamic, neon-glowing ropes between your fingertips, simulating gravity and inertia in a low-latency environment.

---

## 🚀 Core Features

- **Bilateral Hand Tracking**  
  Detects and tracks 10 individual fingertip anchors across two hands simultaneously.

- **Verlet Integration Physics**  
  Custom physics engine handles segment constraints and gravity for realistic "rope" behavior.

- **Neural Aesthetics**  
  Features a multi-layered rendering pipeline with:
  - Anti-Aliased Polylines for smooth visuals  
  - Sine-Wave Pulsing glow animation  
  - High-intensity white core for realistic light simulation  

- **Hardware Optimized**  
  Uses NumPy vectorization to maintain high FPS even on standard CPUs.

---

## 🛠️ Installation & Setup

### 1. Environment Requirements
- Python 3.8 or higher  
- Webcam (required for real-time tracking)

### 2. Dependencies

```bash
pip install opencv-python mediapipe numpy
▶️ Usage
python neon_tracking.py
To Quit: Press q while the display window is active.

💡 Tip: Works best in high-contrast lighting (bright hands, darker background).

🧠 Technical Deep-Dive
The Physics Engine: Verlet Integration

Unlike standard Euler integration, this project utilizes Verlet Integration to maintain distance constraints between rope segments. This prevents unrealistic stretching and ensures simulation stability.

The position update formula:

xₙ₊₁ = xₙ + (xₙ − xₙ₋₁) + a · Δt²

Where:

(xₙ − xₙ₋₁) = velocity (momentum from previous frame)
a = acceleration (gravity)
Δt = timestep

Constraint satisfaction is handled through iterative distance correction between segments.

📊 Thread Configuration
Parameter	Default Value	Impact
Segments	12 - 15	Higher = smoother motion, Lower = stiffer ropes
Friction	0.98	Energy retention (1.0 = no damping)
Gravity	0.5	Downward force on threads
Pulse Frequency	tick * 0.2	Speed of neon glow pulsing
🎨 Visual Pipeline

The neon effect is rendered in two stages:

Aura Layer
Anti-aliased polyline
Width modulated with sin() for pulsing glow
Filament Core
Thin white line (1px)
Simulates high-energy light center

⚠️ Important

The code currently targets fingertip landmarks:
4, 8, 12, 16, 20

To track different joints, modify the tips_indices list in the configuration section.

🤝 Contributing

Contributions are welcome!

Fork the project

Create your branch

git checkout -b feature/AmazingFeature

Commit your changes

git commit -m "Add some AmazingFeature"

Push to GitHub

git push origin feature/AmazingFeature
Open a Pull Request
📜 License

Distributed under the MIT License. See LICENSE for more information.

⚠️ Disclaimer

This project is experimental and may require manual camera exposure adjustments depending on your hardware.

# Watercolorinator (a Doofenshmirtz-inspired name)
### 🚧 [Work In Progress]

Watercolorinator is a tool for watercolor enthusiasts, designed by **MalaMdg**.  
It helps artists **simulate color blends**, **convert images into watercolor styles**, and **generate painting instructions**.

## 🎨 Features
- **📸 Picture to Watercolor** → Convert any image into a simulated watercolor painting.
- **🖌️ Painting Instructions** → Get step-by-step guidance on how to paint an image.
- **🌈 Pigment Database** → Store and analyze real-world pigments.
- **🔬 Pigment Blender** → Simulate watercolor blending based on brush strokes and pigment interaction.

## 🛠️ Current Development Progress
✅ **Core Modules Implemented**
- 📁 **Image Handling** → Load and process images (`image_handler.py`)
- 🎨 **Color Extraction & Visualization** → Extract dominant colors and plot them in 3D (`color_viewer.py`)
- 📝 **Configuration System** → Centralized JSON-based config (`config.py`)
- 📜 **Logging System (RFC 5424 Compliant)** → Structured logging for debugging (`logger.py`)

🛠 **Upcoming Features**
- 🎭 **Color Reduction & Optimization**
- 🎨 **Advanced Watercolor Simulation**
- 📖 **Painting Instruction Generator**
- 🖍 **Real Pigment Data Integration**

## 🚀 How to Run
1. Clone the repository:
   ```sh
   git clone https://github.com/Malamdg/watercolorinator.git
   cd watercolorinator
   ```
2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
3. Run the color extraction and visualization module:
    ```sh
    python src/color_viewer.py
    ```
4. (WIP) Convert an image into a watercolor simulation:
    ```sh
    python src/app.py
    ```
## 📜 License
This project is open-source under the **MIT License**.

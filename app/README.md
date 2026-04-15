# Speed Radar Application
A desktop application for real-time speed measurement and leaderboard management, designed to work with a radar-based embedded system via UART

### 📌 Overview
This application provides:  
- real-time speed visualization
- measurement session handling
- leaderboard management
- communication with microcontroller via UART

### 🧠 Architecture
The application follows a modular architecture:  
```text
app/  
├───config.py           # configuration
├───main.py             # entry point
├───requirements.txt    # dependencies
├───assets/             # logos
├───core/               # logic and communication
└───ui/                 # GUI (CustomTkinter)
```

### Modules
- UI (`ui/`)
  - Handles user interface and interaction
  - Displays speed, timer and leaderboard
- Core (`core/`)
  - `serial_reader.py` → UART communication
  - `session.py` → measurement logic
  - `leaderboard.py` → results storage (CSV)
- Assets (`assets/`)
  - logos used in GUI

### ⚙️ Requirements
- Python 3.10+
- Serial connection to microcontroller

### Python dependencies
```text
customtkinter  
pyserial  
pillow  
```

### 🚀 Installation & Run
1. Clone repository  
   ```bash
   git clone <repo-url>
   cd app
   ```
2. Create virtual environment (optional)  
   **Windows**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   **Linux / macOS**  
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Configure application  
   The application is configured at runtime via terminal input.  

   After launching the program, you will be prompted to provide:  
     - Serial Port  
       Example:  
         - Windows: `COM3`, `COM5`
         - Linux: `/dev/ttyUSB0`, `/dev/ttyACM0`
     - Baud Rate:  
       Must match the microcontroller configuration.  
       Example:  
       `115200`
     - Results File
       Path to CSV file used for storing leaderboard data.  
       Example:  
       `results.csv`
5. Run application  
   ```bash
   python main.py
   ```
    
### 🎮 Usage
1. Enter your name
2. Click **START NEW SESSION**
3. Perform the measurement
4. Click **FINISH AND SAVE**
5. Result is added to the leaderboard

### 🔌 UART Communication
The application expects the microcontroller to send:  
- ASCII text
- numeric speed values (e.g. `16.6`)
- the value must be sent in format `%.1f\r\n`

### 💾 Data Storage
- Results are stored in a CSV file
- Automatically loaded on startup
- Sorted by highest speed

  Example:  
  name,speed  
  Alice,25.4  
  Bob,22.1

### 🧩 Features
- real-time speed display
- session timer
- max speed tracking
- persistent leaderboard
- modular architecture

### ⚠️ Notes
- Make sure the correct COM port is selected
- Ensure the microcontroller is sending valid numeric data
- If no data appears, verify UART connection and firmware
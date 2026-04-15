import customtkinter as ctk
from PIL import Image
import threading
import time

from core.serial_reader import SerialReader
from core.leaderboard import Leaderboard
from core.session import Session
from config import *

class SpeedChallengerApp(ctk.CTk):
    """
    Main GUI application for Speed Challenge system.

    Responsibilities:
    - Handles user interface (Tkinter / CustomTkinter)
    - Manages user interactions (start sessio, save result)
    - Displays real-time speed data
    - Communication with backend modules:
        - SerialReader (UART communication)
        - Session (measurement logic)
        - Leaderboard (data storage)

    This class acts as an orchestrator between UI and core logic. 
    """
    
    def __init__(self):
        """Initialize application, logic modules and start background thread."""
        super().__init__()

        # window configuration
        self.title("Speed Challenge 2026")
        self.geometry("900x500")
        self.resizable(True, True)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # core modules
        self.serial = SerialReader(PORT, BAUDRATE)
        self.serial.connect()

        self.leaderboard = Leaderboard(RESULTS_FILE)
        self.session = Session(SESSION_DURATION)

        self.running = True # controls UART thread loop

        # UI setup
        self.setup_ui()
        self.update_leaderboard_ui()

        # background thread
        threading.Thread(target=self.read_uart, daemon=True).start()

    def setup_ui(self):
        """Create and layout all GUI elements (frames, labels, buttons)."""
        # load images
        self.micro_logo = self.load_image(MICRO_PATH)
        self.wiet_logo = self.load_image(WIET_PATH)

        # layout configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # left panel
        self.left_frame = ctk.CTkFrame(self, corner_radius=15)
        self.left_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.logos_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        self.logos_frame.pack(fill="x", padx=20, pady=10)

        if self.micro_logo:
            self.micro_logo = ctk.CTkLabel(self.logos_frame, image=self.micro_logo, text="")
            self.micro_logo.pack(side="right", padx=5)

        if self.wiet_logo:
            self.wiet_logo = ctk.CTkLabel(self.logos_frame, image=self.wiet_logo, text="")
            self.wiet_logo.pack(side="left", padx=5)

        self.label_name = ctk.CTkLabel(self.left_frame, text="NAME:", font=("Arial", 16))
        self.label_name.pack(pady=(20, 5))

        self.entry_name = ctk.CTkEntry(self.left_frame, placeholder_text="ENTER YOUR NAME...", width=200)
        self.entry_name.pack(pady=5)

        self.btn_start = ctk.CTkButton(
            self.left_frame,
            text="START NEW SESSION",
            command=self.start_session,
            fg_color="green",
            hover_color="#006400"
        )
        self.btn_start.pack(pady=10)

        self.speed_display = ctk.CTkLabel(
            self.left_frame,
            text="0.0",
            font=("Consolas", 100, "bold"),
            text_color="#00E676"
        )
        self.speed_display.pack(pady=10)

        self.timer_label = ctk.CTkLabel(
            self.left_frame,
            text="TIME: 0.0s",
            font=("Arial", 30, "bold"),
            text_color="#FFD600"
        )
        self.timer_label.pack(pady=(0, 10))

        self.max_label = ctk.CTkLabel(
            self.left_frame,
            text="YOUR MAX SPEED: 0.0 km/h",
            font=("Arial", 20, "italic")
        )
        self.max_label.pack(pady=5)

        self.btn_save = ctk.CTkButton(
            self.left_frame,
            text="FINISH AND SAVE",
            command=self.save,
            state="disabled"
        )
        self.btn_save.pack(pady=20)

        # right panel
        self.right_frame = ctk.CTkFrame(self, corner_radius=15)
        self.right_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.label_top = ctk.CTkLabel(
            self.right_frame,
            text="🏆 LEADERBOARD",
            font=("Arial", 24, "bold")
        )
        self.label_top.pack(pady=15)

        self.scrollable_leaderboard = ctk.CTkScrollableFrame(
            self.right_frame,
            width=350,
            height=300
        )
        self.scrollable_leaderboard.pack(padx=10, pady=10, fill="both", expand=True)

    def load_image(self, path):
        """
        Load and resize image for GUI display.

        Returns:
            CTKImage or None if loading fails.
        """
        try:
            if path == MICRO_PATH:
                return ctk.CTkImage(
                    light_image=Image.open(path),
                    dark_image=Image.open(path),
                    size=(150, 150)
                )
            if path == WIET_PATH:
                return ctk.CTkImage(
                    light_image=Image.open(path),
                    dark_image=Image.open(path),
                    size=(100, 100)
                )
        except:
            print(f"IMAGE ERROR: {path}")
            return None

    def start_session(self):
        """
        Start a new measurement session.

        - Validates user input (name)
        - Resets session state
        - Enables measurement and UI updates
        """
        name = self.entry_name.get().strip()
        if not name:
            self.entry_name.focus()
            return

        self.session.start()
        self.current_name = name

        self.speed_display.configure(text="0.0")
        self.max_label.configure(text=f"SESSION: {name}")

        self.btn_save.configure(state="normal")
        self.btn_start.configure(state="disabled")
        self.entry_name.configure(state="disabled")

        self.update_timer()

    def update_timer(self):
        """
        Update session countdown timer.

        Called periodically using Tkinter's `after()` method.
        Stops when session duration is reached.
        """
        if not self.session.active:
            return

        remaining = self.session.remaining()

        if remaining > 0:
            self.timer_label.configure(text=f"TIME: {remaining:.1f}s")
            self.after(50, self.update_timer)
        else:
            self.session.stop()
            self.timer_label.configure(text="FINISH!", text_color="#FF3D00")
            self.max_label.configure(
                text=f"YOUR MAX: {self.session.max_speed:.1f} km/h"
            )

    def read_uart(self):
        """
        Background thread function.

        Continuously reads data from UART and forwards it to GUI.
        """
        while self.running:
            val = self.serial.read_value()
            if val is not None and self.session.active:
                self.after(0, self.process_value, val)
            time.sleep(0.01)

    def process_value(self, val):
        """
        Process new speed value from UART.

        Args:
            val (float): Measured speed value
        """
        self.speed_display.configure(text=f"{val:.1f}")
        self.session.update(val)

        self.max_label.configure(
            text=f"RECORD: {self.session.max_speed:.1f} km/h"
        )

    def save(self):
        """
        Save current session result to leaderboard.

        - Adds new score
        - Writes to CSV
        - Refreshes UI
        """
        self.leaderboard.add(self.current_name, self.session.max_speed)
        self.leaderboard.save()

        self.update_leaderboard_ui()

        self.session.stop()

        self.btn_save.configure(state="disabled")
        self.btn_start.configure(state="normal")
        self.entry_name.configure(state="normal")
        self.entry_name.delete(0, "end")

    def update_leaderboard_ui(self):
        """Refresh leaderboard display in GUI."""
        for widget in self.scrollable_leaderboard.winfo_children():
            widget.destroy()

        for i, entry in enumerate(self.leaderboard.data):
            color = "#FFD700" if i == 0 else "white"

            row = ctk.CTkLabel(
                self.scrollable_leaderboard,
                text=f"{i + 1}. {entry['name']} - {entry['speed']:.1f} km/h",
                font=("Arial", 16),
                text_color=color
            )
            row.pack(anchor="w", pady=2)

    def destroy(self):
        """Cleanup resources on app close."""
        self.running = False
        self.serial.close()
        super().destroy()
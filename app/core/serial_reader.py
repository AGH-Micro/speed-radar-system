import serial

class SerialReader:
    """
    Handles UART communication with the microcontroller.

    Responsibilities:
    - Establish serial connection (COM port, baudrate)
    - Read incoming data from UART
    - Parse received data into numeric speed values

    This class abstracts low-level serial communication from the rest of the system.
    """

    def __init__(self, port, baudrate):
        """
        Initialize SerialReader.

        Args:
            port (str): Serial port (e.g. COM3)
            baudrate (int): Communication speed
        """
        self.port = port
        self.baudrate = baudrate
        self.serial_port = None

    def connect(self):
        """
        Open serial communication.

        Prints error message if connection fails.
        """
        try:
            self.serial_port = serial.Serial(self.port, self.baudrate, timeout=1)
        except:
            print(f"COM ERROR. CANNOT OPEN SERIAL PORT {self.port}")
    
    def read_value(self):
        """
        Read and parse a single value from UART.

        Returns:
            float or None:
                - float: parsed speed value
                - None: if no valid data received
        """
        if self.serial_port and self.serial_port.is_open:
            try:
                line = self.serial_port.readline().decode('utf-8').strip()
                if line:
                    return float(''.join(filter(lambda x: x.isdigit() or x == '.', line)))
            except:
                return None
        return None

    def close(self):
        """Close serial connection."""
        if self.serial_port:
            self.serial_port.close()
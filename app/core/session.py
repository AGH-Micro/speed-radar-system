import time

class Session:
    """
    Represents a single measurement session.

    Responsibilities:
    - Track session state (active / inactive)
    - Measure elapsed time
    - Store and update maximum speed

    This class contains pure logic (no UI, no I/O)
    """

    def __init__(self, duration):
        """
        Initialize session.
        
        Args:
            duration (float): Session duration in seconds
        """
        self.duration = duration
        self.active = False
        self.start_time = None
        self.max_speed = 0

    def start(self):
        """
        Start a new session.

        Resets maximum speed and initializes timer.
        """
        self.active = True
        self.start_time = time.time()
        self.max_speed = 0

    def stop(self):
        """Stop current session."""
        self.active = False

    def update(self, value):
        """
        Update session with new speed value.

        Args:
            value (float): Current speed

        Updates:
            max_speed if new_value is higher.
        """
        if value > self.max_speed:
            self.max_speed = value

    def remaining(self):
        """
        Calculate remaining session time.

        Returns:
            float: Remaining time in seconds (>= 0)
        """
        if not self.active:
            return 0
        return self.duration - (time.time() - self.start_time)
    
    def is_finished(self):
        return self.remaining() <= 0
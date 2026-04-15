import csv
import os

class Leaderboard:
    """
    Stores and manages leaderboard data.

    Responsibilities:
    - Store player results (name + speed)
    - Load/save results from/to CSV file
    - Sort results by best score

    This class is responsible only for data persistence and sorting.
    """

    def __init__(self, file):
        """
        Initialize leaderboard.

        Args:
            file (str): Path to CSV file
        """
        self.file = file
        self.data = []
        self.load()

    def add(self, name, speed):
        """
        Add new result to leaderboard.

        Args:
            name (str): Player name
            speed (float): Achived speed

        Automatically sorts leaderboard after insertion.
        """
        self.data.append({"name": name, "speed": speed})
        self.data.sort(key=lambda x: x["speed"], reverse=True)
        
    def save(self):
        """
        Save leaderboard data to CSV file.

        Overwrites existing file.
        """
        try:
            with open(self.file, mode="w", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["name", "speed"])
                writer.writeheader()
                writer.writerows(self.data)
        except Exception as e:
            print(f"WRITE ERROR IN FILE: {e}")

    def load(self):
        """
        Load leaderboard data from CSV file.

        Converts speed values to float.
        Ignores invalid rows.
        """
        if os.path.exists(self.file):
            try:
                with open(self.file, mode="r", encoding="utf-8") as file:
                    reader = csv.DictReader(file)
                    self.data = [{"name": r["name"], "speed": float(r["speed"])} for r in reader]
            except Exception as e:
                print(f"READ ERROR IN FILE {e}")
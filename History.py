

import csv
import os
from datetime import datetime
from core.constants import HISTORY_FILE

CSV_HEADERS = ["Date", "Name", "BMI", "Category",
               "Weight", "Weight Unit", "Height", "Height Unit"]


def save_result(name: str, bmi: float, category: str,
                weight: float, weight_unit: str,
                height: float, height_unit: str) -> None:
    """Append a new BMI result row to the history CSV."""
    file_exists = os.path.isfile(HISTORY_FILE)
    with open(HISTORY_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(CSV_HEADERS)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            name, bmi, category,
            weight, weight_unit,
            height, height_unit,
        ])


def load_history() -> list[dict]:
    if not os.path.isfile(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        return list(csv.DictReader(f))


def clear_history() -> None:
    """Delete the history CSV file entirely."""
    if os.path.isfile(HISTORY_FILE):
        os.remove(HISTORY_FILE)

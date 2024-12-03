import csv
import json
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class DataWriter:
    @staticmethod
    def save_csv(data: List[Dict], filepath: str) -> bool:
        """Save data as CSV file."""
        try:
            if not data:
                return False
                
            with open(filepath, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            return True
        except Exception as e:
            logger.error(f"CSV writing error: {str(e)}")
            return False

    @staticmethod
    def save_json(data: List[Dict], filepath: str) -> bool:
        """Save data as JSON file."""
        try:
            with open(filepath, 'w') as file:
                json.dump(data, file, indent=2)
            return True
        except Exception as e:
            logger.error(f"JSON writing error: {str(e)}")
            return False
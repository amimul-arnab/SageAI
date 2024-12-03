import csv
import json
import logging
from pathlib import Path
from typing import List, Dict

class DataWriter:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def save_csv(self, data: List[Dict], filepath: str) -> bool:
        try:
            output_path = Path(filepath)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            fieldnames = ['term', 'complicated_text', 'simplified_definition', 'analogy', 'mind_map_prompt']
            
            with open(output_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            return True
            
        except Exception as e:
            self.logger.error(f"CSV write error: {str(e)}")
            return False

    def save_json(self, data: List[Dict], filepath: str) -> bool:
        try:
            output_path = Path(filepath)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            formatted_data = []
            for item in data:
                formatted_item = {
                    "term": item["term"],
                    "complicated_text": item["complicated_text"],
                    "simplified_definition": item["simplified_definition"],
                    "analogy": item["analogy"],
                    "mind_map_prompt": item["mind_map_prompt"]
                }
                formatted_data.append(formatted_item)
                
            with open(output_path, 'w', encoding='utf-8') as file:
                json.dump(formatted_data, file, indent=2, ensure_ascii=False)
            return True
            
        except Exception as e:
            self.logger.error(f"JSON write error: {str(e)}")
            return False
import json
from pathlib import Path

CONFIG = {
    "data_file": "data/operations.xlsx",
    "report_dir": "data/reports"
}

def load_json_config():
    config_path = Path("config.json")
    if config_path.exists():
        with open(config_path) as f:
            return {**CONFIG, **json.load(f)}
    return CONFIG
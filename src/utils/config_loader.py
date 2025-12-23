import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
CONFIG_PATH = os.path.join(src_dir, "config.json")

DEFAULT_CONFIG = {
    "leaf_sensor_count": 5,
    "force_mock_mode": False,
    "serial_port": "AUTO",
    "filter_window_size": 5,
    "force_retrain": False
}

def load_config(file_path=CONFIG_PATH):
    if not os.path.exists(file_path):
        return calculate_derived(DEFAULT_CONFIG)

    try:
        with open(file_path, 'r') as f:
            user_config = json.load(f)
        
        config = DEFAULT_CONFIG.copy()
        config.update(user_config)
        return calculate_derived(config)
        
    except json.JSONDecodeError:
        return calculate_derived(DEFAULT_CONFIG)

def save_config(config_dict, file_path=CONFIG_PATH):
    save_data = {k: v for k, v in config_dict.items() if k in DEFAULT_CONFIG}
    
    with open(file_path, 'w') as f:
        json.dump(save_data, f, indent=4)

def calculate_derived(config):
    config["total_sensors"] = 2 + config["leaf_sensor_count"]
    return config
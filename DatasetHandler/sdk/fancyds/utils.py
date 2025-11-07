import numpy as np
from typing import Dict, Any

def convert_np_to_lists(data: Dict[str, Any]) -> Dict[str, Any]:
    for k, v in data.items():
        if isinstance(v, np.ndarray):
            data[k] = v.tolist()
        elif isinstance(v, dict):
            data[k] = convert_np_to_lists(v)
        elif isinstance(v, list):
            data[k] = [convert_np_to_lists(item) if isinstance(item, dict) else item for item in v]
    return data
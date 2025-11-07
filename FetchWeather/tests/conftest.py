import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tests.fixtures.core import client, sample_weather_data, test_config, test_db

import pytest
from drone_simulator import Drone  # your SIL API or stub
from drone_simulator import Mode
import logging
import os
##standard drone at mission status at home position
@pytest.fixture
def drone():
    battery_start_level=0.50
    wind_speed=30
    mode=Mode.STANDBY
    v = Drone(battery_start_level,wind_speed,mode)
    yield v
    v.shutdown()

@pytest.fixture(scope="class", autouse=True)
def log():
    print("Working directory:", os.getcwd())

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler("RTHtest.log", mode="w")
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger



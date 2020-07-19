from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class Prediction:
    label: str
    probability: float


@dataclass
class ObjectRecognition:
    uid = str
    event_id: str
    catalog_id: str
    created_time = datetime
    predictions = List[Prediction]


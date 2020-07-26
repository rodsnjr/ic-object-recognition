from dataclasses import dataclass
from datetime import datetime
from typing import List
import json


@dataclass
class Prediction:
    label: str
    probability: float

    def to_dict(self):
        return dict(
            label=self.label,
            probability=str(self.probability)
        )


@dataclass
class ObjectRecognition:
    uid: str
    event_id: str
    catalog_id: str
    created_time: datetime
    predictions: List[Prediction]

    def has_predictions(self, labels: List[str]):
        return any(map(lambda x: x.label in labels, self.predictions))

    def predictions_json(self) -> str:
        predictions_list = list(map(lambda x: x.to_dict(),
                                    self.predictions))
        return json.dumps(predictions_list)

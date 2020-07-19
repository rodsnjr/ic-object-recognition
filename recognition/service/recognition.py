from typing import List

from tflite_runtime.interpreter import Interpreter
import numpy as np
from recognition.domain import ObjectRecognition, Prediction
from recognition.providers import Resource
import time


# InceptionV4 Model with TFLite
class Inception:
    def __init__(self):
        self._model = None
        self._labels = None
        self._width = None
        self._height = None
        self._input_mean = None
        self._input_std = None
        self._floating_model = None
        self._input_details = None
        self._output_details = None

    @property
    def model(self):
        if self._model is None:
            self._model = Interpreter(Resource.inception)
            self._model.allocate_tensors()
        return self._model

    @property
    def labels(self):
        if self._labels is None:
            with open(Resource.inception_labels, 'r') as f:
                self._labels = [line.strip() for line in f.readlines()]
        return self._labels

    @property
    def input_details(self):
        if self._input_details is None:
            self._input_details = self.model.get_input_details()
        return self._input_details

    @property
    def output_details(self):
        if self._output_details is None:
            self._output_details = self.model.get_output_details()
        return self._output_details

    @property
    def floating_model(self):
        if self._floating_model is None:
            self._floating_model = self.input_details[0]['dtype'] == np.float32
        return self._floating_model

    @property
    def width_height(self):
        if self._width is None:
            self._width = self.input_details[0]['shape'][2]

        if self._height is None:
            self._height = self.input_details[0]['shape'][1]
        return self._width, self._height

    def _process_image(self, img):
        width, height = self.width_height
        img = img.resize((width, height))

        # add N dim
        input_data = np.expand_dims(img, axis=0)

        if self.floating_model:
            input_data = (np.float32(input_data) - self._input_mean) / self._input_std

        return input_data

    def _process_output(self):
        output_data = self.model.get_tensor(self.output_details[0]['index'])
        results = np.squeeze(output_data)
        top_k = results.argsort()[-5:][::-1]
        for i in top_k:
            if self.floating_model:
                yield Prediction(
                    probability=float(results[i]),
                    label=self.labels[i]
                )
            else:
                yield Prediction(
                    probability=float(results[i] / 255.0),
                    label=self.labels[i]
                )

    def predict(self, img) -> List[Prediction]:
        input_data = self._process_image(img)
        self.model.set_tensor(self.input_details[0]['index'], input_data)

        start_time = time.time()
        self.model.invoke()
        stop_time = time.time()
        print('Inception Predict Time: {:.3f}ms'.format((stop_time - start_time) * 1000))

        return list(self._process_output())


def recognize(image) -> ObjectRecognition:
    pass


async def save(object_recognition: ObjectRecognition):
    pass


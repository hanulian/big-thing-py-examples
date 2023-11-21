"""
This is an example of using the k-nearest-neighbors (KNN) algorithm for face recognition.

When should I use this example?
This example is useful when you wish to recognize a large set of known people,
and make a prediction for an unknown person in a feasible computation time.

Algorithm Description:
The knn classifier is first trained on a set of labeled (known) faces and can then predict the person
in an unknown image by finding the k most similar faces (images with closet face-features under euclidean distance)
in its training set, and performing a majority vote (possibly weighted) on their label.

For example, if k=3, and the three closest face images to the given image in the training set are one image of Biden
and two images of Obama, The result would be 'Obama'.

* This implementation uses a weighted vote, such that the votes of closer-neighbors are weighted more heavily.

Usage:

1. Prepare a set of images of the known people you want to recognize. Organize the images in a single directory
   with a sub-directory for each known person.

2. Then, call the 'train' function with the appropriate parameters. Make sure to pass in the 'model_save_path' if you
   want to save the model to disk so you can re-use the model without having to re-train it.

3. Call 'predict' and pass in your trained model to recognize the people in an unknown image.

NOTE: This example requires scikit-learn to be installed! You can install it with pip:

$ pip3 install scikit-learn

"""

import os
import time
import pickle
from typing import List, Set, Tuple, Any
from dataclasses import dataclass, asdict, field

import numpy as np
import cv2
import face_recognition
from sklearn import neighbors


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


@dataclass
class FaceModel:
    encodings: list = field(default_factory=list)
    names: list = field(default_factory=list)
    knn: neighbors.KNeighborsClassifier = None
    trained_persons: Set[str] = field(default_factory=set)


# TODO: Add exception handling for cases when multiple faces are detected.
class FaceRecognizer:
    def __init__(self, dataset_path: str = 'dataset', model_path: str = 'model.pkl', threshold: float = 0.3) -> None:
        self.dataset_path = dataset_path
        self.model_path = model_path
        self.model: FaceModel = FaceModel()
        self.threshold = threshold

        self._load_model(self.model_path)

    def _save_model(self, model_path: str) -> None:
        with open(model_path, 'wb') as file:
            pickle.dump(asdict(self.model), file)

    def _load_model(self, model_path: str) -> None:
        if os.path.exists(model_path):
            with open(model_path, 'rb') as file:
                data = pickle.load(file)
                self.model = FaceModel(**data)

    def train(self) -> None:
        for person in os.listdir(self.dataset_path):
            # if person is already trained, then skip it
            if person in self.model.trained_persons:
                print(f'{person} is already trained. Skip...')
                continue

            person_path = os.path.join(self.dataset_path, person)

            for image_name in os.listdir(person_path):
                print(f'training {person} from {image_name}...')
                image_path = os.path.join(person_path, image_name)
                image = face_recognition.load_image_file(image_path)
                face_locations = face_recognition.face_locations(image)
                face_encodings = face_recognition.face_encodings(image, known_face_locations=face_locations)

                self.model.encodings.extend(face_encodings)
                self.model.names.extend([person] * len(face_encodings))

            self.model.trained_persons.add(person)

        if len(self.model.encodings) > 0 or len(self.model.names) > 0:
            knn = neighbors.KNeighborsClassifier(n_neighbors=1, metric="euclidean")
            knn.fit(self.model.encodings, self.model.names)
        else:
            knn = None

        self.model.knn = knn
        self._save_model(self.model_path)

    def recognize(self, image_path: str) -> list:
        if not os.path.isfile(image_path) or os.path.splitext(image_path)[1][1:] not in ALLOWED_EXTENSIONS:
            raise Exception(f'Invalid image path: {image_path}')

        image = face_recognition.load_image_file(image_path)
        return self.recognize_from_frame(image)

    def recognize_from_frame(self, image: np.ndarray) -> List[Tuple[str, Tuple[int, int, int, int]]]:
        if len(self.model.trained_persons) == 0:
            print('Trained face is empty! If you are running this app for the first time, run `add_face` first.')
            return []

        knn = self.model.knn
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, known_face_locations=face_locations)
        closest_distances = knn.kneighbors(face_encodings, n_neighbors=1)
        are_matches = [closest_distances[0][i][0] <= self.threshold for i in range(len(face_locations))]

        result = [
            (pred, loc) if rec else ('unknown', loc)
            for pred, loc, rec in zip(knn.predict(face_encodings), face_locations, are_matches)
        ]

        if result == []:
            return [('unknown', (0, 0, 0, 0))]

        return result

    def check_face_exist(self, name: str) -> bool:
        if self.model is None:
            return False

        return name in self.model.names

    def detect_face(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        face_locations = face_recognition.face_locations(image)
        return face_locations

    def add_face(self) -> None:
        cam = cv2.VideoCapture(0)
        count = 0
        tmp_person_name = '_TMP'
        capture_num = 10
        # fps = 30
        # sleep_time = 1.0 / fps
        while count < capture_num:
            ret, frame = cam.read()
            if not ret:
                continue

            face_location = self.detect_face(frame)
            for top, right, bottom, left in face_location:
                cropped = frame[top:bottom, left:right]
                os.makedirs(os.path.join(self.dataset_path, tmp_person_name), exist_ok=True)
                tmp_dataset_path = os.path.join(self.dataset_path, tmp_person_name, f'image_{count}.jpg')
                cv2.imwrite(tmp_dataset_path, cropped)
                print(f'face capture to {tmp_dataset_path} complete...')
                count += 1

            # time.sleep(sleep_time)
        cam.release()
        print(f'face capture complete! - {capture_num} images captured')

        name = input(f'Name: ')
        if not self.check_face_exist(name):
            dataset_path = os.path.join(self.dataset_path, name)
            os.makedirs(dataset_path, exist_ok=True)
            for image_name in os.listdir(os.path.join(self.dataset_path, tmp_person_name)):
                os.rename(
                    os.path.join(self.dataset_path, tmp_person_name, image_name), os.path.join(dataset_path, image_name)
                )
            self.train()
        else:
            print(f'face {name} already exist')

    def delete_face(self, name: str) -> None:
        self.model.trained_persons.remove(name)
        index_list = [i for i, n in enumerate(self.model.names) if n == name]
        self.model.encodings = [
            list(encodings) for j, encodings in enumerate(self.model.encodings) if j not in index_list
        ]
        self.model.names = [name for j, name in enumerate(self.model.names) if j not in index_list]

        if len(self.model.encodings) > 0 or len(self.model.names) > 0:
            knn = neighbors.KNeighborsClassifier(n_neighbors=1, metric="euclidean")
            knn.fit(self.model.encodings, self.model.names)
        else:
            knn = None

        self.model.knn = knn
        self._save_model(self.model_path)

    def result_to_person(self, result: List[Tuple[str, Tuple[int, int, int, int]]]) -> str:
        person_list = []
        for name, location in result:
            top, right, bottom, left = location
            print(f'- Found {name} at ｢({left}, {top}), ({right}, {bottom})｣')
            person_list.append(name)

        if len(person_list) == 0:
            return 'unknown'

        if len(person_list) > 1:
            print(f'Found multiple faces: {person_list}. return first one: {person_list[0]}')

        return person_list[0]


if __name__ == '__main__':
    recognizer = FaceRecognizer(dataset_path='dataset', model_path='model.clf')
    recognizer.train()

    for image_file in os.listdir('test_img'):
        full_file_path = os.path.join('test_img', image_file)
        result = recognizer.recognize(full_file_path)
        person = recognizer.result_to_person(result)
        print(f'{person} from {full_file_path}')

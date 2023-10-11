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

import math
from sklearn import neighbors

# from sklearn.neighbors import KNeighborsClassifier
import os
import os.path
import pickle
from PIL import Image, ImageDraw
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import numpy as np

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def train(
    train_dir: str,
    model_save_path: str = None,
    n_neighbors: int = None,
    knn_algo: str = 'ball_tree',
    verbose: bool = False,
    force_retrain: bool = False,
):
    """
    Trains a k-nearest neighbors classifier for face recognition.

    :param train_dir: directory that contains a sub-directory for each known person, with its name.

     (View in source code to see train_dir example tree structure)

     Structure:
        <train_dir>/
        ├── <person1>/
        │   ├── <somename1>.jpeg
        │   ├── <somename2>.jpeg
        │   ├── ...
        ├── <person2>/
        │   ├── <somename1>.jpeg
        │   └── <somename2>.jpeg
        └── ...

    :param model_save_path: (optional) path to save model on disk
    :param n_neighbors: (optional) number of neighbors to weigh in classification. Chosen automatically if not specified
    :param knn_algo: (optional) underlying data structure to support knn.default is ball_tree
    :param verbose: verbosity of training
    :return: returns knn classifier that was trained on the given data.
    """
    X: list = []
    y: list = []

    # Load a pre-trained KNN classifier (if one was passed in)
    if model_save_path is not None:
        try:
            with open(model_save_path, 'rb') as f:
                print(f'Load pretrained KNN model...')
                knn_clf = pickle.load(f)
                X = list(knn_clf._fit_X)
                y = list(knn_clf.classes_)
        except FileNotFoundError:
            pass

    # Loop through each person in the training set
    for class_dir in os.listdir(train_dir):
        if not os.path.isdir(os.path.join(train_dir, class_dir)):
            continue

        # Loop through each training image for the current person
        for img_path in image_files_in_folder(os.path.join(train_dir, class_dir)):
            # Avoid duplicating training data
            if img_path in y and not force_retrain:  # Assuming the img_path is unique for each image
                if verbose:
                    print(f'Skipping {img_path}, already in training data')
                continue

            image = face_recognition.load_image_file(img_path)
            face_bounding_boxes = face_recognition.face_locations(image)

            if len(face_bounding_boxes) != 1:
                # If there are no people (or too many people) in a training image, skip the image.
                if verbose:
                    error_msg = "Didn't find a face" if len(face_bounding_boxes) < 1 else "Found more than one face"
                    print(f'Image {img_path} not suitable for training: {error_msg}')
            else:
                # Add face encoding for current image to the training set
                face_encode = face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0]
                X.append(face_encode)
                y.append(img_path)

    # Determine how many neighbors to use for weighting in the KNN classifier
    if n_neighbors is None:
        n_neighbors = int(round(math.sqrt(len(X))))
        if verbose:
            print('Chose n_neighbors automatically:', n_neighbors)

    # Create and train the KNN classifier
    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
    knn_clf.fit(X, y)

    # Save the trained KNN classifier
    if model_save_path is not None:
        with open(model_save_path, 'wb') as f:
            pickle.dump(knn_clf, f)

    return knn_clf


def predict(X_img_path, knn_clf=None, model_path=None, distance_threshold=0.6):
    """
    Recognizes faces in given image using a trained KNN classifier

    :param X_img_path: path to image to be recognized
    :param knn_clf: (optional) a knn classifier object. if not specified, model_save_path must be specified.
    :param model_path: (optional) path to a pickled knn classifier. if not specified, model_save_path must be knn_clf.
    :param distance_threshold: (optional) distance threshold for face classification. the larger it is, the more chance
           of mis-classifying an unknown person as a known one.
    :return: a list of names and face locations for the recognized faces in the image: [(name, bounding box), ...].
        For faces of unrecognized persons, the name 'unknown' will be returned.
    """
    if not os.path.isfile(X_img_path) or os.path.splitext(X_img_path)[1][1:] not in ALLOWED_EXTENSIONS:
        raise Exception(f'Invalid image path: {X_img_path}')

    if knn_clf is None and model_path is None:
        raise Exception('Must supply knn classifier either thourgh knn_clf or model_path')

    # Load a trained KNN model (if one was passed in)
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)

    # Load image file and find face locations
    X_img = face_recognition.load_image_file(X_img_path)
    X_face_locations = face_recognition.face_locations(X_img)

    # If no faces are found in the image, return an empty result.
    if len(X_face_locations) == 0:
        return []

    # Find encodings for faces in the test iamge
    faces_encodings = face_recognition.face_encodings(X_img, known_face_locations=X_face_locations)

    # Use the KNN model to find the best matches for the test face
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]

    # Predict classes and remove classifications that aren't within the threshold
    return [
        (pred, loc) if rec else ('unknown', loc)
        for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)
    ]


def show_prediction_labels_on_image(img_path, predictions):
    """
    Shows the face recognition results visually.

    :param img_path: path to image to be recognized
    :param predictions: results of the predict function
    :return:
    """
    pil_image = Image.open(img_path).convert('RGB')
    draw = ImageDraw.Draw(pil_image)

    for name, (top, right, bottom, left) in predictions:
        # Draw a box around the face using the Pillow module
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

        # There's a bug in Pillow where it blows up with non-UTF-8 text
        # when using the default bitmap font
        name = name.encode('UTF-8')

        # Draw a label with a name below the face
        text_width, text_height = draw.textsize(name)
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
        draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))

    # Remove the drawing library from memory as per the Pillow docs
    del draw

    # Display the resulting image
    pil_image.show()


class FaceRecognizer:
    def __init__(self, dataset_path: str = 'dataset', model_path: str = 'model.pkl', threshold: float = 0.3) -> None:
        self.dataset_path = dataset_path
        self.model_path = model_path
        self.encodings = []
        self.names = []
        self.knn = None
        self.trained_persons = set()
        self.threshold = threshold

        self.load_model()

    def train(self) -> None:
        current_encodings = []
        current_names = []

        for person in os.listdir(self.dataset_path):
            if person in self.trained_persons:
                print(f'{person} is already trained. Skip...')
                continue

            person_path = os.path.join(self.dataset_path, person)

            for image_name in os.listdir(person_path):
                print(f'training {person} from {image_name}...')
                image_path = os.path.join(person_path, image_name)
                image = face_recognition.load_image_file(image_path)
                face_locations = face_recognition.face_locations(image)
                face_encodings = face_recognition.face_encodings(image, known_face_locations=face_locations)

                current_encodings.extend(face_encodings)
                current_names.extend([person] * len(face_encodings))

            self.trained_persons.add(person)

        self.encodings.extend(current_encodings)
        self.names.extend(current_names)

        self.knn = neighbors.KNeighborsClassifier(n_neighbors=1, metric="euclidean")
        self.knn.fit(self.encodings, self.names)

        self.save_model()

    def recognize(self, image_path: str) -> list:
        if not os.path.isfile(image_path) or os.path.splitext(image_path)[1][1:] not in ALLOWED_EXTENSIONS:
            raise Exception(f'Invalid image path: {image_path}')

        if self.knn is None and self.model_path is None:
            raise Exception('Must supply knn classifier either though knn_clf or model_path')

        image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, known_face_locations=face_locations)
        closest_distances = self.knn.kneighbors(face_encodings, n_neighbors=1)
        are_matches = [closest_distances[0][i][0] <= self.threshold for i in range(len(face_locations))]

        result = [
            (pred, loc, image_path) if rec else ('unknown', loc, image_path)
            for pred, loc, rec in zip(self.knn.predict(face_encodings), face_locations, are_matches)
        ]
        return result

    def save_model(self) -> None:
        data = {
            'encodings': self.encodings,
            'names': self.names,
            'knn': self.knn,
            'trained_persons': self.trained_persons,
        }
        with open(self.model_path, 'wb') as file:
            pickle.dump(data, file)

    def load_model(self) -> None:
        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as file:
                data = pickle.load(file)
                self.encodings = data['encodings']
                self.names = data['names']
                self.knn = data['knn']
                self.trained_persons = data.get('trained_persons', set())

    def check_face_exist(self, name: str) -> bool:
        return name in self.names


if __name__ == '__main__':
    recognizer = FaceRecognizer(dataset_path='dataset', model_path='model.clf')
    recognizer.train()

    for image_file in os.listdir('test_img'):
        full_file_path = os.path.join('test_img', image_file)
        predictions = recognizer.recognize(full_file_path)
        for name, (top, right, bottom, left), image_path in predictions:
            print(f'- Found {name} at ({left}, {top}) in {image_path}')

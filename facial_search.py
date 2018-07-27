import os
import glob
import face_recognition


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def facial_search(image_to_test):
    name = None
    status = False
    image_dir = "image_subset/"
    test_image = face_recognition.load_image_file(image_to_test)
    known_face_encodings = []
    known_face_names = []
    if os.path.exists(image_dir):
        for filename in glob.iglob(os.path.join(image_dir, '*jpg'), recursive=True):
            print(filename)
            image = face_recognition.load_image_file(filename)
            image_face_encoding = face_recognition.face_encodings(image)[0]
            known_face_encodings.append(image_face_encoding)
            child_id = filename.split("/")[-1].split(".")[0]
            known_face_names.append(child_id)

    face_locations = face_recognition.face_locations(test_image)
    face_encodings = face_recognition.face_encodings(test_image, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)

        name = None
        status = False

        # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            status = True

    return name, status


if __name__ == '__main__':
    print(facial_search("temp/test.jpg"))

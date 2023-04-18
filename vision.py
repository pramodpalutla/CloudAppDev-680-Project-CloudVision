from google.cloud import vision, storage
from google.protobuf.json_format import MessageToJson
from firebase_admin import credentials, db
import firebase_admin
import tempfile
import os
import uuid
import json

vision_client = vision.ImageAnnotatorClient()
storage_client = storage.Client()

def initFirebase():
    bucket_name = 'imgdata-in'
    json_file_name = 'cis680-project-firebase-adminsdk-7z62f-f711deec96.json'
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.get_blob(json_file_name)
    json_data = blob.download_as_text()
    credentials_dict = json.loads(json_data)
    cred = credentials.Certificate(credentials_dict)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://cis680-project-default-rtdb.firebaseio.com'
    })


def detect_face(data, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    initFirebase()
    file_data = data

    file_name = file_data["name"]
    bucket_name = file_data["bucket"]
    print(f"Processing file: {file_name}.")
    print(f"Bucket: {bucket_name}.")

    blob = storage_client.bucket(bucket_name).get_blob(file_name)
    blob_uri = f"gs://{bucket_name}/{file_name}"
    blob_source = vision.Image(source=vision.ImageSource(
        gcs_image_uri=blob_uri))

    faces = vision_client.face_detection(image=blob_source,
                                         max_results=4).face_annotations
    print(faces)

    if len(faces) > 0:
        uploadToGCS(faces, file_name)


def uploadToGCS(faces, file_name):
    faces_dict = []

    for face in faces:
        face_dict = {
            'bounding_poly': {
                'vertices': [{
                    'x': vertex.x,
                    'y': vertex.y
                } for vertex in face.bounding_poly.vertices]
            },
            'landmarks': [{
                'type': landmark.type_,
                'position': {'x': landmark.position.x, 'y': landmark.position.y, 'z': landmark.position.z}
            }for landmark in face.landmarks],
            'roll_angle': face.roll_angle,
            'pan_angle': face.pan_angle,
            'tilt_angle': face.tilt_angle,
            'detection_confidence': face.detection_confidence,
            'joy_likelihood': face.joy_likelihood,
            'sorrow_likelihood': face.sorrow_likelihood,
            'anger_likelihood': face.anger_likelihood,
            'surprise_likelihood': face.surprise_likelihood,
            'under_exposed_likelihood': face.under_exposed_likelihood,
            'blurred_likelihood': face.blurred_likelihood,
            'headwear_likelihood': face.headwear_likelihood,
            'landmarking_confidence': face.landmarking_confidence,

        }
        faces_dict.append(face_dict)
    _, temp_local_filename = tempfile.mkstemp()

    f = open(temp_local_filename, "w")

    f.write(json.dumps(faces_dict))
    f.close()

    face_bucket = storage_client.bucket("imgdata-out")
    uploadfilename = file_name + "-res.json"
    new_blob = face_bucket.blob(uploadfilename)
    new_blob.upload_from_filename(temp_local_filename)
    print(f"Face Response uploaded to: gs://{face_bucket}/{uploadfilename}")

    os.remove(temp_local_filename)
    face_id = str(uuid.uuid4())
    ref = db.reference('/facial_data')
    facial_data = {
        "facial_data_path" : f"gs://imgdata-out/{uploadfilename}",
        "image_path": f"gs://imgdata-in/{file_name}"
    }
    ref.child(face_id).set(facial_data)
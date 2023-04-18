import json
from google.cloud import vision

def detect_face(request):
    # Get the image URL from the request
    request_json = request.get_json()
    if 'image_url' not in request_json:
        return 'No image URL found in request', 400
    image_url = request_json['image_url']

    # Initialize the Cloud Vision API client
    client = vision.ImageAnnotatorClient()

    # Create an image object with the image URL as the source
    image = vision.types.Image()
    image.source.image_uri = image_url

    # Use the Cloud Vision API to perform face detection on the image
    response = client.face_detection(image=image, max_results=4)
    faces = response.face_annotations
    
    if len(faces) > 0:
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
        json_result = json.dumps(faces_dict)

        return json_result

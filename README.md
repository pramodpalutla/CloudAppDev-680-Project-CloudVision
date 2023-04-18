# SAI PALUTLA
# CloudVision-CIS680-Project

> Prerequisites - This guide assumes you have prior experience setting up projects using the technologies involved.
## To recreate this project in Google Cloud, follow these steps:

1. Create a new project in the Google Cloud Console.
2. Enable the following APIs:
    - Cloud Functions API
    - Cloud Storage API
    - Cloud Vision API
3. Create a new project in the Firebase Console and enable Firebase Realtime Database API
4. Set up a Firebase Realtime Database and note the database URL and secret key. You will need these later to authenticate with the database.
5. Set up a Cloud Storage bucket to store the uploaded images. Note the bucket name and location.
6. Set up a Cloud Storage bucket to store the json data of the images. Note the bucket name and location.
7. Create a new Cloud Function with the following settings:
    - Runtime: Python 3.7
    - Trigger: Cloud Storage
    - Event Type: Finalize/Create
    - Bucket: <your bucket name>
    - Source code: Copy and paste the code for the imgProc function from the project repository (https://github.com/saipalutla/gcp-image-processing/blob/main/functions/index.js)
    - Add the following to requirements.txt file
        - `google-cloud-vision==2.6.1`
        - `google-cloud-storage==1.42.2`
        - `firebase-admin`
8. Create another Cloud Function with the following settings:
    - Runtime: Python 3.7
    - Trigger: Cloud Storage
    - Event Type: HTTP
    - Allow Unauthenticated Invocations
    - Source code: Copy and paste the code for the imgProc function from the project repository (https://github.com/saipalutla/gcp-image-processing/blob/main/functions/index.js)
    - Add the following to requirements.txt file
        - `google-cloud-vision==2.6.1`
        - `google-cloud-storage==1.42.2`
        - `firebase-admin`

8. Set up a Cloud API Gateway to expose the Cloud Function as an API. Note the API Gateway URL.
9. Test the first cloud function with the cloud storage trigger by uploading an image to the Cloud Storage bucket
10. Test the second cloud function by making a POST request to the API Gateway URL. You should receive a JSON object containing the facial data extracted from the image.

> Note: You will need to have a Google Cloud account and billing enabled to use the above services.
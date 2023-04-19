# SAI PALUTLA
# CloudVision-CIS680-Project

> Demo Video
>> [![](https://markdown-videos.deta.dev/youtube/KWXMnNukZBg)](https://youtu.be/KWXMnNukZBg)

> Prerequisites - This guide assumes you have prior experience setting up projects using the following Google Cloud products:
> 1. Cloud Vision
> 2. Cloud Functions
> 3. Cloud Storage
> 4. Firebase Realtime Database
> 5. Cloud API Gateway
## To recreate this project in Google Cloud, follow these steps:

1. Create a new project in the Google Cloud Console.
2. Enable the following APIs:
    - Cloud Functions API
    - Cloud Storage API
    - Cloud Vision API
3. Create a new project in the Firebase Console and enable Firebase Realtime Database API
4. Set up a Firebase Realtime Database and note the database URL and secret key. You will need these later to authenticate with the database.
5. Follow these steps to generate Firebase service account credentials JSON file.
    - Go to the Firebase Console and select your project.
    - Click on the gear icon in the top left corner to open the project settings.
    - Select the "Service Accounts" tab.
    - Click on the "Generate New Private Key" button to download the JSON file containing your credentials.
    - Save the JSON file securely on your local machine.
    - In your Cloud Functions code, use the Firebase Admin SDK to initialize with your service account credentials.
5. Set up a Cloud Storage bucket to store the uploaded images. Note the bucket name and location.
6. Set up a Cloud Storage bucket to store the json data of the images. Note the bucket name and location.
7. Create a new Cloud Function with the following settings:
    - Runtime: Python 3.7
    - Trigger: Cloud Storage
    - Event Type: Finalize/Create
    - Bucket: <your bucket name>
    - Source code: Copy and paste the code for the imgProc function from the project repository [vision.py](vision.py)
    - Update the bucket names in the code to match the name of the buckets created
    - Add the following to requirements.txt file
        - `google-cloud-vision==2.6.1`
        - `google-cloud-storage==1.42.2`
        - `firebase-admin`
8. Create another Cloud Function with the following settings:
    - Runtime: Python 3.7
    - Trigger: Cloud Storage
    - Event Type: HTTP
    - Allow Unauthenticated Invocations
    - Source code: Copy and paste the code for the imgProc function from the project repository [vision_rest.py](vision_rest.py)
    - Update the bucket names in the code to match the name of the buckets created
    - Add the following to requirements.txt file
        - `google-cloud-vision==2.6.1`
        - `google-cloud-storage==1.42.2`
        - `firebase-admin`

8. Set up a Cloud API Gateway to expose the Cloud Function as an API. Note the API Gateway URL.
9. Test the first cloud function with the cloud storage trigger by uploading an image to the Cloud Storage bucket
10. Test the second cloud function by making a POST request to the API Gateway URL. You should receive a JSON object containing the facial data extracted from the image.

> Note: You will need to have a Google Cloud account and billing enabled to use the above services.
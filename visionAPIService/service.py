from __future__ import print_function
from google.cloud import vision
import os, io
from flask import Flask
from flask import request

# Create flask server
app = Flask(__name__)


# Define route
@app.route('/')
def get_labels():
    path_to_image = request.args.get('path', type=str)
    print(path_to_image)

    # Set GoogleVisionAPI service token
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ServiceToken.json"

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    file_name = os.path.abspath(path_to_image)

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    # Print the detected labels
    print('Labels:')
    data = []
    for label in labels:
        data.append(label.description)
        print(label.description)

    # Check if one of the following labels is contained in answer
    if "Face" in data or "Standing" in data or "Jeans" in data or "Jacket" in data or "Zipper" in data or "Denim" in data or "Sleeve" in data or "Trousers" in data:
        return "True"
    else:
        return "False"


app.run()

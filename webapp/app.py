import base64

import cv2 as cv2
import numpy as np
from flask import Flask, render_template, request, jsonify
from keras.engine.saving import load_model

"""
Cathal Butler | G00346889 | Emerging Technologies Project 
This class handles starting a Flask application which then handles API requests send from the client view. 
The frontend allows users draw a number between 0 -> 9 on a canvas that will then be processed below to meet the 
requirements needed to to a prediction of the number agents a trained model. The predicted number is then sent back 
to the user. 

Reference:
https://www.jitsejan.com/python-and-javascript-in-flask.html
https://blog.keras.io/building-a-simple-keras-deep-learning-rest-api.html
https://stackoverflow.com/questions/45408496/getting-error-cannot-reshape-array-of-size-122304-into-shape-52-28-28
https://github.com/tensorflow/tensorflow/issues/28287#issuecomment-495005162
http://yangyang.blog/2019/03/it-works-an-epic-debugging-thesis-week-8/
https://stackoverflow.com/questions/53653303/where-is-the-tensorflow-session-in-keras
https://stackoverflow.com/questions/30963705/python-regex-attributeerror-nonetype-object-has-no-attribute-group/30964049
https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/clearRect
"""

# initialize Flask application
app = Flask(__name__)


# GET ROUTE which will return a render of the index.html page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# GET, POST ROUTE which will allow a POST request of input canvas data to be processed and then returned
@app.route('/predict', methods=['POST', 'GET'])
def post_predict():
    # ensure an image was properly uploaded to our endpoint
    if request.method == 'POST':
        # read data from request
        data_url = request.values['data_url_string']

        print(data_url)
        # remove unneeded data from the start of the data URL and convert the bytes into an image
        convert_to_image(data_url)

        # read image into memory
        image = cv2.imread('input_digit.png')
        # convert the image to gray scale
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # make it the right size of 28x28
        image = prepare_image(image, size=(28, 28))
        # reshape the array
        image = np.array(image).reshape((1, 28, 28, 1))

        # Load the trained model
        model = load_model('model.h5')

        # Make a predication with of the image agents tbe trained model
        prediction = model.predict(image)

        # Use np.argmax to return the highest number from the array. In theory it should be the number drawn in the
        predicted_number = np.argmax(prediction)

        # convert ndarray to list to be send in the response
        prediction = np.array(prediction).tolist()

        try:
            # Return the prediction data to the webapp
            return jsonify({'prediction': prediction, 'predicted_number': str(predicted_number)})
        except:
            # return failed is script does not process data correctly
            return jsonify({'prediction': "failed!"})


# Function to resize the image the 28x28 and flatten the image received in the POST request
def prepare_image(img, size=(28, 28)):
    return cv2.resize(img, size).flatten()


# Function to convert the data sent in the data url to an image. It will ignore the first 22 bits of the data as that
# needed to decode the image
def convert_to_image(image_data):
    print(image_data[22:])
    # Decode the image & save the image
    with open('input_digit.png', 'wb') as f:
        # data_url[24:] using everything in the array after 24
        f.write(base64.b64decode(image_data[22:]))


# Running application on localhost:5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
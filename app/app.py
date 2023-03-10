from flask import Flask, request, Response 
from flask_uploads import UploadSet, IMAGES, configure_uploads
import jsonpickle
import pickle
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas
import numpy
import matplotlib
import tensorflow
app = Flask(__name__)

# Load the pickled data and store it in a global variable
with open('final_model.sav', 'rb') as f:
    model = pickle.load(f)


# Configure the app to store uploaded files in the 'uploads' folder
app.config['UPLOADS_DEFAULT_DEST'] = 'vol1'

# Create an UploadSet for handling image uploads
images = UploadSet('images', IMAGES)

# Configure the Flask-Uploads extension
configure_uploads(app, (images,))

filename = ''






@app.route('/api/test', methods=['GET'])
def test():
    # Model code
    response = {'message': 'API hit iimv'}
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route('/api/upload', methods=['POST'])
def upload():
    # Check if a file was uploaded
    if 'image' not in request.files:
        return 'No file uploaded', 400

    # Save the uploaded file
    # Save the uploaded file
    filename = images.save(request.files['image'])
    img = Image.open(filename)
    img = np.array(img)
    
    #results = cv.detect_common_objects(img, model='yolov3')
   
    
    preds = model.predict(img)
    
    masked_images = preds * img
    
    plt.subplot(3, 4, 2)
    plt.axis(False)
    plt.grid(False)
     results= plt.imshow(masked_images)
     my_string = str(results)

    # Return the filename of the saved file
    return my_string, 200
    
    
    
    
    






if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

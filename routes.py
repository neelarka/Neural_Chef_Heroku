
from flask import Flask, jsonify, render_template, url_for, request, redirect
import json
import os
import glob
from models import PredictRawVeggies


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
my_pred = PredictRawVeggies()


# # Define routes ###############################################################
@app.route("/",  methods=['GET', 'POST'])
def index():
    print("upload click")
    if request.method == 'POST':
        print("POST click")
        if request.files.get('file'):
            print("File is there")
#
            images = request.files.getlist("file") #convert multidict to dict
            print(f"Images: {images}")
            # Remove all the files
            files = glob.glob(app.config['UPLOAD_FOLDER']+'/*')
            # print(files)
            for f in files:
                os.remove(f)

            filenames = []
            #save the image
            for image in images:     #image will be the key
                # create a path to the uploads folder
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
                image.save(filepath)
                filenames.append(image.filename)
                print(filenames)

            predictions = my_pred.call_predict(filenames, app.config['UPLOAD_FOLDER'])

        return jsonify({'result': 'success', 'predictions': predictions})
        # return ('', 204)
    # print(my_pred.labels)
    return render_template('index.html')

#####################################################################################
@app.route('/update', methods=['POST'])
def update():

    print(f"In update {my_pred.labels}")
    # get the list
    filenames = []
    image_names = request.form.getlist('image[]')

    if (image_names == []):
        filenames = ["No Images to predict"]
        print("No Images to predict")
    else:
        for image_name in image_names:
            filenames.append(image_name.split('\\')[-1:][0])

        predictions = my_pred.call_predict(filenames, app.config['UPLOAD_FOLDER'])
        # print(f"predictions : {predictions}")
        # print(filenames)

    return jsonify({'result': 'success', 'predictions': predictions})

######################################################
# ###########################################################################

if __name__ == '__main__':
    app.run(debug=True)

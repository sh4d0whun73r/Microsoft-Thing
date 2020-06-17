from flask import Flask, render_template, request
import cv2
import tensorflow as tf
import os

app = Flask(__name__, template_folder="templates")

@app.route('/', methods= ["GET", "POST"]) 
def index():
  if request.method== "GET":
    return render_template("index.html")
  else:
    asl = request.form.get("asl")
    CATEGORIES = ['A','B','C','D','del','E','F','G','H','I','J','K','L','M','N','nothing','O','P','Q','R','S','space','T','U','V','W','X','Y','Z']

    def prepare(filepath):
     IMG_SIZE = 65
     img_array = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
     new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
     return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)
     model = tf.keras.models.load_model("64x3-CNN.model")
     prediction = model.predict([prepare('asl')])
     trans = CATEGORIES[int(prediction[0][0])]
     return redirect(url_for('translate', trans = trans, prediction = prediction))
    
@app.route('/translate', methods = ["GET", "POST"])
def translate():
   if request.method== "GET":
    return render_template("translate.html")
   else:
     trans = request.args.get("trans", None)
     prediction = request.args.get("prediction", None)
     return render_template("translate.html", trans = trans, prediction = prediction)

app.run(host='0.0.0.0', port=8080)
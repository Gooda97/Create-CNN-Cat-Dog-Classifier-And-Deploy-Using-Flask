from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import tensorflow as tf
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import os

try:
    import shutil

    shutil.rmtree("uploaded / image")
    print()
except:
    pass

model = tf.keras.models.load_model("model.h5")
app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "uploaded\\image"


@app.route("/")
def upload_f():
    return render_template("upload.html")


import keras

# keras.preprocessing
def finds():
    
    ## There are two ways to predict one of them is used and the other one is commented
    # test_datagen = keras.preprocessing.image.ImageDataGenerator(rescale=1.0 / 255)
    # vals = [
    #     "Cat",
    #     "Dog",
    # ]  # change this according to what you've trained your model to do
    # test_dir = "uploaded"
    # test_generator = test_datagen.flow_from_directory(
    #     test_dir,
    #     target_size=(200, 200),
    #     color_mode="rgb",
    #     shuffle=False,
    #     class_mode="categorical",
    #     batch_size=1,
    # )
    # ----------------------------------------------
    f = request.files["file"]
    img = tf.keras.preprocessing.image.load_img(
        os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(f.filename)),
        target_size=(64, 64),
    )
    img = tf.keras.preprocessing.image.img_to_array(img)
    x = np.expand_dims(img, axis=0)
    images = np.vstack([x])
    cat = "Cat"
    dog = "Dog"
    pred = model.predict_generator(images)
    print(pred)                           
    # print(vals[np.argmax(pred)])
    print(pred[0][0])
    # return str(vals[np.argmax(pred)])
    if pred[0][0] < 0.5:
        return cat
    else:
        return dog     


@app.route("/uploader", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        f = request.files["file"]
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(f.filename)))
        val = finds()
        os.remove(
            os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(f.filename))
        )
        return render_template("pred.html", ss=val)


if __name__ == "__main__":
    app.run()
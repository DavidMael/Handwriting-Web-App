import model.preprocess as pp
import tensorflow as tf
from PIL import Image
import numpy as np

filepath = "putwriting.png"

linebounds = pp.textDetect(filepath)

pp.charSegment(filepath, linebounds)

img = Image.open("character-images/6.png").convert('L')

model = tf.keras.models.load_model("model/letter_model.h5")
model.summary()

img = np.array(img)
val = model.predict(img[None,:,:])
print(val)

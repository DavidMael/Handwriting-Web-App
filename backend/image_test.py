from numpy.core.fromnumeric import transpose
import model.preprocess as pp
import tensorflow as tf
from PIL import Image
import numpy as np

filepath = "putwriting.png"

linebounds = pp.textDetect(filepath)

image_ctr = pp.charSegment(filepath, linebounds)
#image_ctr = 5

model = tf.keras.models.load_model("model/letter_model.h5")
model.summary()

alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v" ,"w", "x", "y", "z"]
blank = np.ones((28, 28))*255

for img_num in range(image_ctr):
    img = Image.open("character-images/"+str(img_num)+".png").convert('L')
    img = np.array(img)
    img = np.transpose(blank - img)

    probs = model.predict(img[None,:,:])

    letter_idx = 0
    letter_prob = 0
    idx = 0
    for val in probs[0]:
        if val > letter_prob:
            letter_idx = idx
            letter_prob = val
        idx = idx + 1

    print(alphabet[letter_idx])
    #print(probs[0])

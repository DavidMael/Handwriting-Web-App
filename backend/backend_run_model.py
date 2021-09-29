from numpy.core.fromnumeric import transpose
import model.preprocess as pp
import tensorflow as tf
from PIL import Image
import numpy as np

class image_reader:

    def __init__(self, modelpath):
        self.model = tf.keras.models.load_model(modelpath)
        self.alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V" ,"W", "X", "Y", "Z"]
        self.blank = np.ones((28, 28))*255

    def read(self, imagepath):

        linebounds = pp.textDetect(imagepath)
        image_ctrs = pp.charSegment(imagepath, linebounds)

        read_string = ""

        start_at = 0
        for line_num in image_ctrs:
            for img_num in range(start_at, line_num, 1):
                img = Image.open("character-images/"+str(img_num)+".png").convert('L')
                img = np.array(img)
                img = np.transpose(self.blank - img)

                probs = self.model.predict(img[None,:,:])

                letter_idx = 0
                letter_prob = 0
                idx = 0
                for val in probs[0]:
                    if val > letter_prob:
                        letter_idx = idx
                        letter_prob = val
                    idx = idx + 1

                read_string = read_string + self.alphabet[letter_idx]

            read_string = read_string + ' '

            start_at = line_num 

        return read_string
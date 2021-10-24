import tensorflow as tf
import tensorflow_datasets as tfds
import numpy as np
import matplotlib.pyplot as plt

def invert_dataset(example):
    tf.enable_eager_execution()
    image = example["image"] / 255
    old_label = example["label"] - 1 
    print(old_label)
    print(old_label[0])
    #print(old_label[0][0])
    print(old_label.numpy()[0])
    zeros = [0] * 26
    zeros[old_label] = 1
    label = tf.constant(zeros)
    return label, image

print(tf.executing_eagerly())

train_data_raw, validation_data_raw = tfds.load("emnist/letters", split = ["train", "test"], shuffle_files=True, batch_size=32)
decoder_train_data = train_data_raw.map(invert_dataset)
decoder_validation_data = validation_data_raw.map(invert_dataset)

decoderModel = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=(26,)),
    tf.keras.layers.Dense(784, activation='relu'),
    tf.keras.layers.Reshape((28, 28))
])
decoderModel.summary()

decoderModel.compile(optimizer="adam",
                    loss=tf.keras.losses.MeanSquaredError())

decoderModel.fit(decoder_train_data, epochs=10,
                validation_data=decoder_validation_data, verbose=1)

#run_single = tf.data.Dataset.from_tensor_slices(tf.constant([0]))
run_single = tf.constant([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
print("------------")
print(run_single.shape())
print("------------")
recreated_letter = decoderModel(run_single).numpy()
plt.figure()
plt.imshow(recreated_letter)
plt.title("reconstructed letter")
plt.gray()
plt.show()
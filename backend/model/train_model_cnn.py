import tensorflow as tf
import tensorflow_datasets as tfds
import numpy
import matplotlib.pyplot as plt

def decrement_label(example):
    image = example["image"] / 255
    label = example["label"] - 1 
    return image, label

train_data_raw, validation_data_raw = tfds.load("emnist/letters", split = ["train", "test"], shuffle_files=True, batch_size=32)
train_data = train_data_raw.map(decrement_label)
validation_data = validation_data_raw.map(decrement_label)

encoderModel = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(64, (5, 5), activation='relu', input_shape=(28, 28, 1)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (4, 4), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(26)
])
encoderModel.summary()

encoderModel.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

history = encoderModel.fit(train_data, epochs=10, 
                    validation_data=validation_data, verbose=1)

print("final model accuracy on training and validation sets:")
encoderModel.evaluate(train_data, verbose = 2)
encoderModel.evaluate(validation_data, verbose = 2)

encoderModel.save("cnn_letter_model.h5")

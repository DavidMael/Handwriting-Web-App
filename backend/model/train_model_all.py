import tensorflow as tf
import tensorflow_datasets as tfds

def decrement_label(example):
    image = example["image"] / 255
    #label = example["label"] - 1 
    label = example["label"]
    return image, label

train_data_raw, validation_data_raw = tfds.load("emnist/byclass", split = ["train", "test"], shuffle_files=True, batch_size=32)
train_data = train_data_raw.map(decrement_label)
validation_data = validation_data_raw.map(decrement_label)

model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28, 1)),
    tf.keras.layers.Dense(250, activation="relu", use_bias=True),
    tf.keras.layers.Dense(250, activation="relu", use_bias=True),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(62, activation="softmax")
])

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

model.fit(train_data, epochs=50, validation_data=validation_data, verbose=1)

print("final model accuracy on training and validation sets:")
model.evaluate(train_data, verbose = 2)
model.evaluate(validation_data, verbose = 2)

model.save("letter_model.h5")
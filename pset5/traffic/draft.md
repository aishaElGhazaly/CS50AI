In a separate file called README.md, document (in at least a paragraph or two) your experimentation process. What did you try? What worked well? What didn’t work well? What did you notice?

load_data()

- Started by looking up how to get a list of directories within a given directory, discovered 2 ways, os.listdir and os.walk, comparing both I cocluded that os.listdir was the suitable method.

- Using nested for loops and os.path.join, i read images in each category_dir using cv2.imread() then resized them to the given dimensions using cv2.resize(). the images were appended to the images list and the label was appended to the labels list

- converted the lists to numpy arrays and returned them as a tuple


get_model()

-1st attempt
I copied the code in handwriting.py and didn't change anything except the input and output shapes to fit this problem. Doing so provided me with a good starting point but truly terrible results.

Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3))
MaxPooling2D((2, 2))
Flatten()
Dense(128, activation="relu")
Dropout(0.5)
Dense(NUM_CATEGORIES, activation="softmax")
optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]

333/333 - 1s - loss: 3.5013 - accuracy: 0.0550 - 1s/epoch - 4ms/step


-2nd attempt
Changing the loss to "binary_crossentropy" slightly improved the accyracy to 0.0568. Still horrible accuracy though.


-3rd attempt

Conv2D(64, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3))
MaxPooling2D((4, 4))
Flatten()
Dense(512, activation="relu")
Dropout(0.5)
Dense(NUM_CATEGORIES, activation="softmax")
optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"]

By changing few parameters such as making the conv2d(64, (3, 3)) instead of conv2d(32, (3, 3)), maxpooling2d((4, 4)) instead of (2, 2) and changing the hidden layer to have 512 units instead of 128, the accuracy shot up to a staggering 94.5% although the training now takes noticably longer time.

333/333 - 2s - loss: 0.0121 - accuracy: 0.9459 - 2s/epoch - 5ms/step


-4th attempt

Conv2D(64, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3))
Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3))
MaxPooling2D((4, 4))
MaxPooling2D((2, 2))
Flatten()
Dense(2048, activation="relu")
Dropout(0.5)
Dense(512, activation="relu")
Dropout(0.5)
Dense(NUM_CATEGORIES, activation="softmax")
optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"]

This setup was a failure. it was too complicated took an enormous amount of time and the accuracy only improved by 1%

333/333 - 5s - loss: 0.0067 - accuracy: 0.9562 - 5s/epoch - 16ms/step


-5th attempt

Using the same config as the third attempt only changing the conv2d to 128 instead of 64 has increased the accuracy by 1% at half the time of the 4th attempt

333/333 - 3s - loss: 0.0123 - accuracy: 0.9518 - 3s/epoch - 8ms/step


-6th attempt
changing maxpool to (2, 2) while keeping conv2d at 64 reaches 95% accuracy but not at the best time.

333/333 - 3s - loss: 0.0135 - accuracy: 0.9534 - 3s/epoch - 10ms/step


-7th attempt
doubling the units of the dense layer to 1024 with a 64 conv2d and (4, 4) hurts the accuracy by about 2%

333/333 - 2s - loss: 0.0147 - accuracy: 0.9368 - 2s/epoch - 7ms/step


-8th attempt
halving the units of the dense layer to 256 with a 64 conv2d and (4, 4) hurts the accuracy by about 4% but it's considerably faster than the previous model.

333/333 - 1s - loss: 0.0183 - accuracy: 0.9148 - 1s/epoch - 5ms/step


-9th attempt

tf.keras.layers.Conv2D(
    64, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
),
tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
tf.keras.layers.Conv2D(
    128, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
),
tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
tf.keras.layers.Flatten(),
tf.keras.layers.Dense(512, activation="relu"),
tf.keras.layers.Dropout(0.5),
tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")

this configuration is nothing short of stellar, i decided to try adding anpther layer of conv2d and maxpool where i double the conv2d to 128 but keep the pool to (2, 2). it reached 98& accuracy with phenomenal time.

333/333 - 5s - loss: 0.0052 - accuracy: 0.9806 - 5s/epoch - 14ms/step


-10th attempt

used the same configuration as the 9th attempt but added another conv2d (32) and maxpool before the 64. it halved the time but brought down the accuracy to 96%

333/333 - 2s - loss: 0.0089 - accuracy: 0.9612 - 2s/epoch - 6ms/step


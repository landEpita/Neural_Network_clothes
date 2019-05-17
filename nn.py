import numpy as np
import sys
import tensorflow as tf
from preprocessing import *
import random

def training():
    rd = random.randint(0,50000)
    print(rd)
    fashion_mnist = tf.keras.datasets.fashion_mnist
    (images, targets), (images_test, targets_test) = fashion_mnist.load_data()
    images = images[rd:rd+10000]
    targets = targets [rd:rd+10000]

    return (images, targets)


class network:
    def __init__(self):
#        self.model = tf.keras.models.Sequential()

        # Add the layers

        img_rows, img_cols = 28, 28
        input_shape = (img_rows, img_cols, 1)
        self.model = tf.keras.models.Sequential() #cree la sequence d'operation

        self.model.add(tf.keras.layers.Conv2D(32, kernel_size=(5, 5), strides=(1, 1),activation='relu',input_shape=input_shape))
        self.model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        self.model.add(tf.keras.layers.Conv2D(64, (5, 5), activation='relu'))
        self.model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))

        self.model.add(tf.keras.layers.Flatten()) # on applatie l img



 #       self.model.add(tf.keras.layers.Flatten(input_shape=[28,28])) # o
        self.model.add(tf.keras.layers.Dense(256, activation="relu"))
        self.model.add(tf.keras.layers.Dense(128, activation="relu"))
        self.model.add(tf.keras.layers.Dense(10, activation="softmax"))

        self.model.compile(
            loss="sparse_categorical_crossentropy",
            optimizer="sgd",
            metrics=["accuracy"]
        )

    def train(self,x,y):
        self.model.fit(x, y, epochs=10)

    def eval(self,x, y):
        self.model.evaluate(x,y)

    def run(self, x):
        return self.model.predict(x)

    def resume(self):
        self.model.summary()

    def save(self, name):
        model_json = self.model.to_json()
        with open(name+"_model.json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        self.model.save_weights(name+".h5")

        print("Saved model to disk")

    def load_save(self, json_file, weight_file):
        json_file = open(json_file, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.model = tf.keras.models.model_from_json(loaded_model_json)
        # load weights into new model
        self.model.load_weights(weight_file)
        self.model.compile(
            loss="sparse_categorical_crossentropy",
            optimizer="sgd",
            metrics=["accuracy"]
        )
        #print("Loaded model from disk")


def main():
    model = network()
    model.load_save("save_model.json","save.h5")
    while(True):
        image, target = training()
        image = image.reshape(image.shape[0], 28, 28, 1)

        model.train(image, target)
        model.save("save")

#main()


